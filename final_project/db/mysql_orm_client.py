import sqlalchemy
from sqlalchemy.orm import sessionmaker


class MysqlOrmConnection:

    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = '0.0.0.0'
        self.port = 3306

        self.engine = None
        self.connection = self.connect()

        session = sessionmaker(bind=self.connection.engine,
                               autoflush=True,
                               enable_baked_queries=False,
                               expire_on_commit=True)
        self.session = session()

    def get_connection(self, db_created=False):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(user=self.user,
                                                                          password=self.password,
                                                                          host=self.host,
                                                                          port=self.port,
                                                                          db=self.db_name if db_created else ''),
            encoding='utf8'
        )
        self.engine = engine
        return engine.connect()

    def get_engine(self):
        return self.engine

    def connect(self):
        connection = self.get_connection()
        connection.close()

        return self.get_connection(db_created=True)

    def execute_query(self, query):
        res = self.connection.execute(query)
        return res.getchall()
