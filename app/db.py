from mongoengine import connect
from pymongo.database import Database
from pymongo import MongoClient

from app.core.config import settings as conf


def connect_mongoengine():
    connect(db=conf.DATABASE, host=conf.MONGO_CONNECTION_STRING)


def get_pymongo_client(conn_str: str = conf.MONGO_CONNECTION_STRING) -> MongoClient:
    return MongoClient(conn_str, uuidRepresentation="standard")


def get_pymongo_database(
    client: MongoClient,
    database: str = conf.DATABASE,
) -> Database:
    return client[database]


client = get_pymongo_client()
db = get_pymongo_database(client=client)
