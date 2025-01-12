from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from app import db


class AuthUser(db.Model):

    id = Column('id', Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))

    auth0_id = Column('auth0_id', String(50), unique=True)

    name = Column('name', String(50))

    accept_tos = Column('accept_tos', Boolean)

