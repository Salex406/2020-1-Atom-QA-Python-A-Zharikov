import pytest

from mysql_orm_client import MysqlOrmConnection


@pytest.fixture(scope='session')
def mysql_orm_client():
    return MysqlOrmConnection('test', 'root', 'TEST_PYTHON_ORM')
