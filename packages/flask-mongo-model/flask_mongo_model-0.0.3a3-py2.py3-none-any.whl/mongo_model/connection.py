# -*- coding: utf-8 -*-


import logging
from flask import current_app as app
from pymongo import MongoClient
from pymongo.database import Database


app_conn = {}   # Map apps to connections
logger = logging.getLogger(__name__)


class DBConnection(object):
    @classmethod
    def init_conn(cls):
        try:
            db_name = app.config["MONGODB_SETTINGS"].pop('db_name')
            app_conn[app] = Database(MongoClient(**app.config["MONGODB_SETTINGS"]), db_name)
        except KeyError:
            logger.error('Current app has not set configurations for MongoDB!')

    @classmethod
    def get_conn(cls):
        try:
            return app_conn[app]
        except KeyError:
            DBConnection.init_conn()
            return app_conn[app]

    @property
    def client(self):
        return self.get_conn().client

    def __getattr__(self, item):
        return self.get_conn().__getattr__(item)

    def __getitem__(self, item):
        return self.get_conn().__getitem__(item)

conn = DBConnection()
