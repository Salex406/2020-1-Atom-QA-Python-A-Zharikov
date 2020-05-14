from random import randint
import pytest
from orm_model import Prepod, Log
from sqlalchemy import inspect
from mysql_orm_client import MysqlOrmConnection
from orm_builder import MysqlOrmBuilder


class TestOrmMysql:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.mysql: MysqlOrmConnection = mysql_orm_client
        self.builder = MysqlOrmBuilder(mysql_orm_client)

    def test_creation(self):
        self.builder.add_prepod()

        inspector = inspect(self.mysql.get_engine())
        schemas = inspector.get_schema_names()

        assert "prepods" in inspector.get_table_names()
        assert "name" in inspector.get_columns("prepods")[1].values()
        assert "age" in inspector.get_columns("prepods")[2].values()
        assert "start_teaching" in inspector.get_columns("prepods")[3].values()
