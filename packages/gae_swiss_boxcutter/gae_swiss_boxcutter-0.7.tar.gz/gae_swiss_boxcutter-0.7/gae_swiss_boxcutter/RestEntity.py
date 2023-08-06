from google.appengine.api import users
from googleapiclient import discovery
from google.appengine.ext import ndb
from oauth2client import client
from oauth2client import crypt
from urllib import urlencode
import requests
import httplib2
import webapp2
import json
from urllib3 import PoolManager
from urllib3.contrib.appengine import AppEngineManager
from urllib3.contrib.appengine import is_appengine_sandbox


if is_appengine_sandbox():
    # AppEngineManager uses AppEngine's URLFetch API behind the scenes
    http = AppEngineManager()
else:
    # PoolManager uses a socket-level API behind the scenes
    http = PoolManager()


class RestEntity(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.initialize(request, response)
        self.response.content_type = 'application/json'
        self.user_id = None
        self.is_admin = users.is_current_user_admin()
        if users.get_current_user():
            self.user_id = users.get_current_user().user_id()
        else:
            # attempt to login by oauth2 credentials
            oauth2_user_id = self.get_oauth2_user_id()
            get_user_id_from_oauth2_user_id = getattr(
                self, "get_user_id_from_oauth2_user_id", None)
            if oauth2_user_id and callable(get_user_id_from_oauth2_user_id):
                self.user_id = get_user_id_from_oauth2_user_id(
                    oauth2_user_id)
        if not self.user_id:
            self.abort(401)

    def get(self, id):
        results = None
        if not id:
            arguments = get_request_arguments(self.request)
            xs, next_cursor, more = self.entity.get_by_user_id(
                self.user_id, arguments
            )
            items = [x.to_dict() for x in xs] if xs is not None else []
            results = dict(items=items)
            if more and next_cursor:
                arguments['cursor'] = next_cursor.urlsafe()
                link_next = self.request.path_url + '?' + urlencode(arguments)
                results['_links'] = dict(next=link_next)
        else:
            x = self.entity.get_by_id(int(id))
            if not self.is_admin:
                if x.user_id != self.user_id:
                    self.abort(401)
            results = x.to_dict()

        self.response.write(json.dumps(results, indent=4))

    def post(self, id):
        payload = json.loads(self.request.body)
        entities = []
        if type(payload) is list:
            entities = [self.create_entity(x) for x in payload]
        else:
            entities = [self.create_entity(payload)]

        ndb.put_multi(entities)

        result = [x.to_dict() for x in entities]

        self.response.write(json.dumps(result, indent=4))

    def create_entity(self, payload):
        u = str(payload.get('user_id').encode(
            'utf-8')) if 'user_id' in payload else None

        if not self.is_admin:
            if (u is not None) and (u != self.user_id):
                self.abort(401)

            payload['user_id'] = self.user_id
        else:
            if u is None or u == "":
                payload['user_id'] = self.user_id

        created = self.entity(**payload)
        return created

    def delete(self, id):
        m = self.entity.get_by_id(int(id))
        if not m:
            self.abort(404)
        if m.user_id != self.user_id:
            self.abort(401)
        self.entity.key.delete(id)

    def get_oauth2_user_id(self):
        token = self.request.headers.get('Authorization')
        if token:
            auth_type, id_token = token.split(' ')
            # auth_type, credentials = token.split(' ')
            # credentials = client.AccessTokenCredentials(
            #     credentials,
            #     None)
            # http_auth = credentials.authorize(httplib2.Http())
            # service = discovery.build("plus", "v1", http=http_auth)
            # user = service.people().get(userId='me').execute()
            #
            # return user.get('id')
            return get_oauth2_user_id_from_id_token(id_token,
                                                    self.valid_client_ids)


def get_request_arguments(request):
    filters = request.arguments()
    return dict((k, request.get(k)) for k in filters)


def get_oauth2_user_id_from_id_token(id_token, valid_client_ids):
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s"
    response = http.request('GET', url % id_token)

    # response = requests.get(url % id_token)
    # if response.status_code == 200:
    if response.status == 200:
        # idinfo = response.json()
        idinfo = json.loads(response.data.decode('utf-8'))
        try:
            valid_issuers = ['accounts.google.com',
                             'https://accounts.google.com']
            # If multiple clients access the backend server:
            if idinfo['aud'] not in valid_client_ids:
                logging.error("Unrecognized client.")
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in valid_issuers:
                logging.error("Wrong issure.")
                raise crypt.AppIdentityError("Wrong issuer.")
            # if idinfo['hd'] != APPS_DOMAIN_NAME:
            #     raise crypt.AppIdentityError("Wrong hosted domain.")
            return idinfo['sub']
        except crypt.AppIdentityError:
            logging.error("invalid token")
