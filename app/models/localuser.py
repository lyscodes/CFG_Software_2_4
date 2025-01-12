from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app import db
from app.models.user import User

class LocalUser(db.Model):

    id = Column('id', Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))

    #user = relationship("User", back_populates="localuser")

    first_name = Column('first_name', String(50))

    family_name = Column('family_name', String(50))

    password = Column('password', String(50))
