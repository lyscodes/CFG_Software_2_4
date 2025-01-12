from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db
from app.models.user import User

class AuthUser(db.Model):

    id = Column('id', Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))

    #user = relationship("User", back_populates="authuser")

    auth0_id = Column('auth0_id', String(50), unique=True)

    name = Column('name', String(50))
