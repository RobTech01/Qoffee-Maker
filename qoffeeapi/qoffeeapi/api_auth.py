import os
from qoffeeapi.hc_connector import get_connector
from notebook.base.handlers import IPythonHandler
from qoffeeapi.utils import proxy

## Redirect to login page
class HomeconnectLoginHandler(IPythonHandler):    
    def get(self):
        connector = get_connector()
        authorization_redirect_url = connector.get_authorization_url()
        self.redirect(authorization_redirect_url)


## Get authorization code and request an access_token
class HomeconnectCallbackHandler(IPythonHandler):
    def get(self):
        connector = get_connector()
        authorization_code = self.request.query_arguments['code'][0].decode()
        req_access_token_res = connector.request_access_token(authorization_code)
        connector.set_machine()
        proxy(self, req_access_token_res)


## Refresh an access_token
class HomeconnectRefreshHandler(IPythonHandler):
    def get(self):
        connector = get_connector()
        proxy(self, connector.refresh_access_token())