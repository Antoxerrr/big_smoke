import os
from contextvars import ContextVar

from mongoengine import connect
from pymongo import MongoClient

connection: ContextVar[MongoClient] = ContextVar('connection', default=None)


def db_connection() -> MongoClient:
    active_connection = connection.get()
    if not active_connection:
        new_connection = connect(
            db=os.getenv('MONGO_DB_NAME', 'smokingsucks'),
            host=os.getenv('MONGO_HOST', '127.0.0.1'),
            port=int(os.getenv('MONGO_PORT', 27017)),
        )
        connection.set(new_connection)

        return new_connection
    return active_connection
