import os
from datetime import timedelta
from dotenv import load_dotenv


class Config:

    load_dotenv()

    SECRET_KEY=os.getenv('SECRET_KEY')

    PERMANENT_SESSION_LIFETIME=timedelta(minutes=20)

    SESSION_COOKIE_SECURE=True

    SESSION_COOKIE_SAMESITE='Lax'

    SQLALCHEMY_DATABASE_URI=os.getenv('CONNECTION_STRING')
