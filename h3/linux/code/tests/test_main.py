import requests as rq
from requests import exceptions
import pytest


PASSWORD = "centos\n"
NGINX_ADDR = "http://192.168.0.3:81"


def test_root(remote):
    ans = remote.exec_root("whoami")
    assert ans == 'root\n'


def test_nginx_ssh(remote):
    reply = remote.exec_cmd("netstat -tulpan | grep 81 | awk ' {print $4, $6} '")
    assert "81" in reply and "LISTEN" in reply


def test_nginx_http(remote):
    resp = rq.get(NGINX_ADDR, timeout=1)
    assert resp.status_code == 200


def test_nginx_acess(remote):
    n_before = remote.exec_root("cat /var/log/nginx/access.log | awk ' END{print NR} '")
    rq.get(NGINX_ADDR, timeout=1)
    n_after = remote.exec_root("cat /var/log/nginx/access.log | awk ' END{print NR} '")
    last_l = remote.exec_root("cat /var/log/nginx/access.log | awk ' END{print} '")
    assert n_before < n_after and "python-requests" in last_l


def test_firewalld(remote):
    remote.exec_root("firewall-cmd --permanent --zone=public --remove-port 81/tcp")
    remote.exec_root("firewall-cmd --reload")
    nginx_state = remote.exec_cmd("systemctl status nginx")
    with pytest.raises(exceptions.ConnectTimeout):
        assert rq.get(NGINX_ADDR, timeout=1)
    remote.exec_root("firewall-cmd --permanent --zone=public --add-port 81/tcp")
    remote.exec_root("firewall-cmd --reload")
    assert "active (running)" in nginx_state
