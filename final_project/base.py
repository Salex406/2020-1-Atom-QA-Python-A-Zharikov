import pytest
import os
from ui.pages.login import BasePage
from ui.pages.main import MainPage
from db.mysql_orm_client import MysqlOrmConnection
from db.orm_builder import MysqlOrmBuilder


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, request, mysql_orm_client):
        self.driver = driver
        self.mysql: MysqlOrmConnection = mysql_orm_client
        self.builder = MysqlOrmBuilder(mysql_orm_client)
