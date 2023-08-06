import logging
from .model import ModelBase
from .connection import conn
from .fields import MongoField, DateTimeField, StringField, ObjectIDField


logging.basicConfig(level=logging.INFO)
