import os
from pymongo import MongoClient


def get_database():

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(MONGO_CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client["dsa_tracker"]

database = get_database()
