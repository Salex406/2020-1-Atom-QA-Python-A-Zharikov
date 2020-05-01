from orm_model import Base, Prepod, Log
from mysql_orm_client import MysqlOrmConnection


class MysqlOrmBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine
        self.create_prepods()

    def create_prepods(self):
        if not self.engine.dialect.has_table(self.engine, 'prepods'):
            Base.metadata.tables['prepods'].create(self.engine)

    def add_prepod(self):
        prepod = Prepod(
            name="Test",
            age=28,
            start_teaching="2020-09-09"
        )

        self.connection.session.add(prepod)
        self.connection.session.commit()

        return prepod


class MysqlOrmLogBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine
        self.engine = self.connection.engine

    def create_log_db(self):
        if not self.engine.dialect.has_table(self.engine, 'log'):
            Base.metadata.tables['log'].create(self.engine)

    def add_log(self, url, code, method, ip):
        log = Log(
            url=url,
            ip=ip,
            code=code,
            method=method
        )

        self.connection.session.add(log)
        self.connection.session.commit()
        return log
