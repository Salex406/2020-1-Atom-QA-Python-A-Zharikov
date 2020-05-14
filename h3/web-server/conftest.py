import pytest
import requests
import mock
import time
from client import Sock


@pytest.fixture(scope='session')
def mock_server():
    server = mock.run_mock()
    server_host = server._kwargs['host']
    server_port = server._kwargs['port']
    time.sleep(1)
    user = {'username': 'Ilya', 'surname': 'Soldatov'}
    url = f"http://{server_host}:{server_port}/add_user"

    s = Sock(target_host=server_host, target_port=server_port)
    s.post_request('/add_user', 'Ilya', 'Soldatov')

    yield server_host, server_port

    shutdown_url = f'http://{server_host}:{server_port}/shutdown'
    requests.get(shutdown_url)
