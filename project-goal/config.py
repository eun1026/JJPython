# config.py

import os

class Config:
    SECRET_KEY = os.urandom(24)  # 세션을 위한 비밀 키
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # SQLite DB URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 추적 여부
