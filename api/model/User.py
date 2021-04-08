from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, CHAR
from api.base import db


class User(db.Model):
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
    phone_private_verified = Column(Integer)
    disabled = Column(Integer)
    created = Column(TIMESTAMP)
    last_login = Column(TIMESTAMP)
    last_update = Column(TIMESTAMP)
    birthdate = Column(Date)
