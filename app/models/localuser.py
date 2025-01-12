from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db

class LocalUser(db.Model):

    id = Column('id', Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")

    first_name = Column('first_name', String(50))

    family_name = Column('family_name', String(50))

    password = Column('password', String(50))
