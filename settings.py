import os
from datetime import timedelta

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')

    PERMANENT_SESSION_LIFETIME=timedelta(minutes=20)

    SESSION_COOKIE_SECURE=True

    SESSION_COOKIE_SAMESITE='Lax'
