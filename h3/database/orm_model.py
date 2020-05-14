from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Prepod(Base):
    __tablename__ = 'prepods'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    start_teaching = Column(Date, nullable=False, default='2020-01-01')


class Log(Base):
    __tablename__ = 'log'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(50), nullable=False)
    code = Column(Integer, nullable=False)
    method = Column(String(5), nullable=False)
    ip = Column(String(40), nullable=False)
