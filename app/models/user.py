from sqlalchemy import Column, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from app import db

class User(db.Model):

    __tablename__='users'

    id: Mapped[int]= mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship(back_populates="parent")

    username = Column(String(50))

    email = Column(String(50))

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def create(self):
        new_user = User(self.username, self.email)
        db.session.add(new_user)
        db.session.commit()