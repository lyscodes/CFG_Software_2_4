from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from app import db
from app.models.entries import Entries

class User(db.Model):

    id = Column(Integer, primary_key=True)

    username = Column(String(50), unique=True, nullable=True)

    email = Column(String(50), unique=True)

    entries = relationship("Entries", backref="user")

    authuser = relationship("AuthUser", backref="user")

    localuser = relationship("LocalUser", backref="user")