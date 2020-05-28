import pytest
from db.mysql_orm_client import MysqlOrmConnection
import time
import sys
import os


@pytest.fixture(scope='session')
def mysql_orm_client():
    return MysqlOrmConnection('test_qa', 'qa_test', 'BACK')

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.hookimpl
def pytest_configure(config):
    if not hasattr(config, "slaveinput"):
        sys.stderr.write("Start\n")
        os.popen('sudo docker-compose up')
        time.sleep(8)

@pytest.hookimpl
def pytest_unconfigure(config):
    if not hasattr(config, "slaveinput"):
        sys.stderr.write("Finish\n")
        os.popen('sudo docker-compose stop')
