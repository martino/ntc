from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    url = Column(String)

    def __init__(self, url):
        self.url = url

