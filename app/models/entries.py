from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db


class Entries(db.Model):

    id = Column('id', Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")

    entry_date = Column('entry_date', Date)

    emotion = Column('emotion', String(50))

    giph_url = Column('giph_url', String(250))

    choice = Column('choice', String(50))

    content = Column('response', String(500))

    diary_entry = Column('diary_entry', String(500), nullable=True)
