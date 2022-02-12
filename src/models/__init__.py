""" Setting module keep ENV variable"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_CONNECTION = os.environ.get("DATABASE_CONNECTION")
ENV = os.environ.get("ENV")
APP = os.environ.get("APP")
