from sqlalchemy import Column, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from app import db

class User(db.Model):

    id: Mapped[int]= mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")

    username = Column(String(50), unique=True)

    email = Column(String(50), unique=True)