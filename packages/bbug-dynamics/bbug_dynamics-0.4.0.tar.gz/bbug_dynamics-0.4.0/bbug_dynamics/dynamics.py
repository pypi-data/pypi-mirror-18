import adal, httplib, urllib, json, boto3, json, datetime, pytz
from io import StringIO
from decimal import *

class Dynamics:
    def __init__(self,settings):
        self.days_to_delete_old_data = settings['days_to_delete_old_data']
        self.bbug_company_id = settings['bbug_company_id']
        self.settings = settings['dynamics']
        self._token= self.token()
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.messages = []

    def headers(self):
         return { 'Authorization': 'Bearer ' + self._token['accessToken'],
                   'Content-Type': 'application/json; charset=utf-8',
                   'Accept': 'application/json',
                   'OData-Version': 4.0
                  }
    def query(self, path='',params='', body='',http_method='GET'):
        params = urllib.urlencode(params)
        if params!='':
            params = '?' + params

        conn= httplib.HTTPSConnection(self.settings['web_api_resource'])
        request_uri = self.settings['canonical_api_uri'] + self.base_uri() + path + params
        conn.request(http_method,request_uri,body, self.headers() )
        self.response= conn.getresponse()

    def base_uri(self):
        return '/'

    def process_response(self):
        if self.response.status == 200:
            d = self.response.read()
            data=json.loads(d)
            return data['value'] if ('value' in data) else data
        else:
            return { 'error': "Cannot get the " + self.__class__.__name__ + " object(s) from dynamics" }

    def token(self):
        authority_url = ('https://login.microsoftonline.com/' +
                        self.settings['tenant'])

        RESOURCE = 'https://' + self.settings['web_api_resource']

        context = adal.AuthenticationContext(authority_url)

        token = context.acquire_token_with_username_password(
            RESOURCE,
            self.settings['user'],
            self.settings['password'],
            self.settings['client_id'])
        return token

    def find_dynamics_object(self,object_id):
        self.query(path="("+object_id+")")

    def save_dynamics_object(self, body_dict):
        self.query(http_method='POST', body=json.dumps(body_dict))
        if self.response.status==204:
            d = self.response.read()
            return json.loads(d)
        else:
            return { 'error': "Cannot save the " + self.__class__.__name__ + " object in dynamics" }



