#*-*coding:utf8*-*

from json import dumps
from time import time
from tornado import gen
from requests.auth import AuthBase

from requests import get,post
from base import INFO,ERROR,Base

class ImException(Exception):
    pass

class Token:
    
    def __init__(self,token,expires_in):
        self.token = token
        self.expires_in = expires_in + int(time())

    def is_valid(self):
        now = int(time())
        INFO('Im Token Time -- Expire Time[%d] -- Now[%d]' % (self.expires_in,now))
        return now < self.expires_in

    def __str__(self):
        return self.token


class Im(object):

    def __init__(self,org_name,app_name,client_id,client_secret): 
        super(Im,self).__init__()
        self._im_url = 'https://a1.easemob.com'
        self._org_name = org_name
        self._app_name = app_name
        self._client_id = client_id
        self._client_secret = client_secret

        self.reset()

    def reset(self):
        token,expire = self.get_token()
        
        if token and expire:
            self._token = Token(token,expire)
        else:
            raise ImException()

    def _get_api_url(self,api_name):
        return '%s/%s/%s/%s' % (self._im_url,self._org_name,self._app_name,api_name)

    def get_token(self):
        token_url = self._get_api_url('token')
    
        data = {'grant_type':'client_credentials','client_id':self._client_id,'client_secret':self._client_secret}
        header = {'Content-Type':'application/json'}

        INFO('Im GetToken -- Url[%s] -- Data[%s] -- Header[%s]' % (token_url,data,header))

        ret = post(token_url,data = dumps(data),headers = header)

        if ret.status_code == 200:
            ret_json = ret.json()       
            access_token = ret_json['access_token']
            expires_in = ret_json['expires_in']
            INFO('Im -- Token[%s] -- expire[%s]' % (access_token,expires_in))
            return access_token,expires_in
        else:
            ERROR('Im GetToken Error -- Status Code[%d]' % ret.status_code)
            return None,None

    def register(self,username,password):
        register_url = self._get_api_url('users')

        token = 'Bearer %s' % str(self._token)
    
        data = {'username':username,'password':password}
        header = {'Content-Type':'application/json','Authorization':token}

        INFO('Im Register -- Url[%s] -- Data[%s] -- Header[%s]' % (register_url,data,header))

        if self._token.is_valid():
            ret = post(register_url,data = dumps(data),headers = header)  
            INFO('Im Register Success -- ret[%s]' % ret.content)
        else:
            INFO('Token Expire')
            self.reset()

        if ret.status_code == 200:
            return True
        else:    
            ERROR('Im Register Error -- Status Code[%d]' % ret.status_code)
            return False

    def login(self,user_name,password):
       pass 
       
