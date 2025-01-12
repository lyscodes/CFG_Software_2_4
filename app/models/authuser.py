from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db

class AuthUser(db.Model):

    id = Column('id', Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")

    auth0_id = Column('auth0_id', String(50), unique=True)

    name = Column('name', String(50))
