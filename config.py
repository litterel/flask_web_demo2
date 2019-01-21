#encoding: utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:chaoyue@localhost/test_bbs'
SQLALCHEMY_TRACK_MODIFICATIONS = True


