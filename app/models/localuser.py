from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from app import db


class LocalUser(db.Model):

    id = Column('id', Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    first_name = Column('first_name', String(50), nullable=False)

    family_name = Column('family_name', String(50), nullable=False)

    password = Column('password', String(250), nullable=False)

    accept_tos = Column('accept_tos', Boolean, nullable=False)
