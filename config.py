import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Labeeb@2001') # Use your secret key
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Labeeb%402001@localhost/railways'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwtapp'
