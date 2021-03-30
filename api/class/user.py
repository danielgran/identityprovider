from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, Date, TIMESTAMP, CHAR
from api.base import base

class User(base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    name_first = Column(String(45))
    name_last = Column(String(45))
    gender = Column(CHAR(1))
    password = Column(String(200))
    password_lastupdate = Column(TIMESTAMP)
    picture = Column(String(255))
    phone_private = Column(String(45))
    phone_private_verified = Column(Integer(1))
    disabled = Column(Integer(1))
    created = Column(TIMESTAMP)
    last_login = Column(TIMESTAMP)
    last_update = Column(TIMESTAMP)
    birthdate = Column(Date)
