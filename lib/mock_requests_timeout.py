from requests import Response, request
from requests.exceptions import ConnectTimeout
import json


class Mock():
    def __init__(self, timeout_first_ok=3):
        self.timeout_first_ok = timeout_first_ok
        self.request = 0

    def get(self, url, data=None, headers={}):
        self.request += 1
        if self.request < self.timeout_first_ok:
            print(f'Request {self.request} timeout')
            raise ConnectTimeout('Request timed out')
        else:
            response = Response()
            response_file = './lib/webex_teams_response_page1.json'
            with open(response_file,'r') as f:
                mock_response = f.read()
                response._content = mock_response.encode()            
            print(f'Request {self.request} ok:')
            response.status_code = 200
            return response

