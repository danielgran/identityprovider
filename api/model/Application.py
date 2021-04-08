from sqlalchemy import Column, ForeignKey, Integer, String, Date, TIMESTAMP, CHAR
from api.base import db


class Application(db.Model):
    __tablename__ = "application"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(45))
    client_id = db.Column(String(45))

    uris = db.relationship("ApplictionUri", backref="application")


class ApplictionUri(db.Model):
    __tablename__ = "application_redirecturi"
    id = db.Column(Integer, primary_key=True)
    id_application = db.Column(Integer, db.ForeignKey("application.id"), nullable=False)
    redirect_uri = db.Column(String(255), nullable=False)


