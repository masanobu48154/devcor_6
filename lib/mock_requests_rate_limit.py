from requests import Response, request
from requests.exceptions import ConnectTimeout
import json

class Mock():
    def __init__(self, rate_limited=None):
        if rate_limited is None:
            self.rate_limited = []
        else:
            self.rate_limited = rate_limited

        self.request = 0

    def get(self, url, data=None, headers={}):
        self.request += 1
        # print(f'self.request: {self.request} self.rate_limit_first: {self.rate_limited}')
        response = Response()
        if self.request not in self.rate_limited:
            response_file = './lib/webex_teams_response_page1.json'
            with open(response_file,'r') as f:
                mock_response = f.read()
                response._content = mock_response.encode()  
                response.status_code = 200          
            print('Request ok')
        else:
            response.status_code = 429
            response.headers['Retry-After'] = 1
            print(f'Request {self.request} rate limited')
        return response
