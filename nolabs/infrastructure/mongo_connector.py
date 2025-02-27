__all__ = ["mongo_connect"]

from mongoengine import ConnectionFailure, connect, disconnect, get_db

from nolabs.infrastructure.settings import settings

connection = None


def get_connection():
    try:
        return get_db()
    except ConnectionFailure:
        return None


def mongo_connect():
    connection = get_connection()
    if connection is None:
        return connect(host=settings.connection_string)
    return connection


def mongo_disconnect():
    disconnect()
