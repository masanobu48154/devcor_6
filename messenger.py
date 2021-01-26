import json
from urllib.parse import urlparse, parse_qs
import requests
from pprint import pprint
from requests.exceptions import ConnectTimeout
from time import sleep

# API Key is obtained from the Webex Teams developers website.
api_key = 'YjdjOTFjYmUtODcyMy00MTk5LWIzOTQtODQ3NTlkM2NmMjAwYmIxODQzZjEtYTlk_P0A1_d1374410-57f8-4153-ad37-0e3a54fb2fd1'
# roomId is a required parameter when fetching messages, 
# and identifies the space (room) from which the messages will be retrieved.
# roomId can be configured here, or collected by the set_room_id method
room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vYWFiN2VjYzAtZWJlNS0xMWVhLTkwZmEtNTlhZWZlNzEyMDQ0'
# Maximum number of messages per page
max_items = 3
# Webex Teams messages API endpoint
base_url = 'https://api.ciscospark.com/v1/messages'


class Messenger(): 
    def __init__(self, base_url=base_url, api_key=api_key, room_id=room_id, requests=requests, request_retries=3): 
        self.base_url = base_url 
        self.api_key = api_key 
        self.room_id = room_id 
        self.api_url = f'{self.base_url}?roomId={self.room_id}&max={max_items}' 
        self.headers = { 
            "Authorization": f"Bearer {api_key}", 
        } 
        self.requests = requests 
        self.request_retries = request_retries 


    def get_messages(self): 
        """ Get a list of messages in a room.  
        Maximum number of items per page is set to 3 """ 

        tries = 0 
        while True: 
            tries += 1 
            try:
                self.response = self.requests.get(self.api_url, headers=self.headers) 

                # Everything ok? 
                if self.response: 
                    self.print_current_page() 
                    return self.response 

                # If not, should we try again later? 
                if self.response.status_code == 429 and tries < self.request_retries:
                    try:
                        retry_after = int(self.response.headers.get('Retry-After'))
                    except Exception:
                        retry_after = 1
    
                    print(f'Waiting for {retry_after} second(s) ...')
                    sleep(retry_after)
                    continue

                # Throw if not ok (2xx) 
                self.response.raise_for_status() 
  
                # Network timeout, should we retry? 

            except ConnectTimeout:
                if tries < self.request_retries:
                    continue
                else:
                    raise

        return self.response 

    def print_current_page(self): 
        """ Print just the text of the messages  
        on the current page """ 
        for msg in (self.response.json())['items']: 
            print(msg['text']) 
        print()

