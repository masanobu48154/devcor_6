import requests
import unittest
from requests.exceptions import ConnectTimeout, HTTPError
from time import sleep
from lib import mock_requests_timeout
from lib import mock_requests_rate_limit
from messenger import Messenger


class ErrorControl(unittest.TestCase):
    def test_network_no_error(self):
        """ Send a request which will not timeout """
        self.msg = Messenger(requests=mock_requests_timeout.Mock(timeout_first_ok=0))
        self.msg.get_messages()

    def test_network_timeout_throws(self):
        """ Send a request which will raise a ConnectTimeout Exception """
        self.msg = Messenger(requests=mock_requests_timeout.Mock(timeout_first_ok=100))
        self.assertRaises(ConnectTimeout, self.msg.get_messages)


    def test_network_timeout_handled(self):
        """ Send a request which will handle a ConnectTimeout Exception """
        """ Send a request which will handle a ConnectTimeout Exception """
        self.msg = Messenger(requests=mock_requests_timeout.Mock(timeout_first_ok=3))
        self.msg.get_messages()


    def test_rate_limit_throws(self):
        """ Send consecutive requests which will be rate limited by the API server. Should return correct error. """
        self.msg = Messenger(requests=mock_requests_rate_limit.Mock(rate_limited=[1, 2, 3, 4]))
        self.assertRaises(HTTPError, self.msg.get_messages)


    def test_rate_limit_handled(self):
        """ Send consecutive requests. First 2 will be rate-limited but 3rd one should work. """
        self.msg = Messenger(requests=mock_requests_rate_limit.Mock(rate_limited=[1, 2]))
        msgs = self.msg.get_messages()
        self.assertIsNotNone(msgs)
