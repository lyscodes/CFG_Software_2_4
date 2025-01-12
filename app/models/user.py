from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from app import db
from app.models.entries import Entries

class User(db.Model):

    id = Column(Integer, primary_key=True)

    entries = relationship("Entries", back_populates="user")

    username = Column(String(50), unique=True)

    email = Column(String(50), unique=True)