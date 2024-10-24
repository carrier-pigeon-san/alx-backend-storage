#!/usr/bin/env python3
""" A script that updates a topic of a school document based on the name """
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """ Update a document in a collection """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
