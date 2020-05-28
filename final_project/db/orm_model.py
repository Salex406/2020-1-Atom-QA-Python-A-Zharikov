from sqlalchemy import Column, Integer, String
from sqlalchemy.types import SmallInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(16), default='NULL', unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(SmallInteger, default=1)
    active = Column(SmallInteger, default=0)
    start_active_time = Column(DateTime, default=None)
