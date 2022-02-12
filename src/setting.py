""" Setting module keep ENV variable"""
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
ENV = os.environ.get("ENV")
APP = os.environ.get("APP")

# Database
DATABASE_CONNECTION = os.environ.get('DATABASE_CONNECTION',
                                     'postgresql+psycopg2://admin:youknow@0.0.0.0:5433/shopping')
SQLALCHEMY_USERNAME = 'admin'
SQLALCHEMY_PASSWORD = 'youknow'
SQLALCHEMY_DATABASE_NAME = 'shopping'
