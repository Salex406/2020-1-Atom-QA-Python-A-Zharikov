import requests
from client import Sock
import json


class TestFlask:

    def test_valid(self, mock_server):
        server_host, server_port = mock_server
        url = f'http://{server_host}:{server_port}/user/0'
        s = Sock(target_host=server_host, target_port=server_port)
        s.get_request(url)
        payload = json.loads(s.get_ans())
        assert payload['code'] == 200
        assert payload['payload']['surname'] == 'Soldatov'

    def test_invalid(self, mock_server):
        server_host, server_port = mock_server
        url = f'http://{server_host}:{server_port}/user/3'
        s = Sock(target_host=server_host, target_port=server_port)
        s.get_request(url)
        payload = json.loads(s.get_ans())
        assert payload['code'] == 404
