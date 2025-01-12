from sqlalchemy import Column, String, Integer, ForeignKey, Date
from app import db


class Entries(db.Model):

    id = Column('id', Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    entry_date = Column('entry_date', Date, nullable=False)

    emotion = Column('emotion', String(50), nullable=False)

    giphy_url = Column('giphy_url', String(250), nullable=False)

    choice = Column('choice', String(50), nullable=False)

    content = Column('response', String(500), nullable=False)

    diary_entry = Column('diary_entry', String(500), nullable=True)
