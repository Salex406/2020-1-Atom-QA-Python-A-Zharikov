import pytest
from ssh_client.client import SSH


@pytest.fixture(scope='session')
def remote():
    with SSH(hostname='192.168.0.3', username='centos', password='centos', port=2003) as ssh:
        yield ssh
