from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app import db

class User(db.Model):

    id = Column(Integer, primary_key=True)

    username = Column(String(50), unique=True, nullable=True)

    email = Column(String(50), unique=True, nullable=False)

    entries = relationship("Entries", backref="user")

    authuser = relationship("AuthUser", backref="user")

    localuser = relationship("LocalUser", backref="user")