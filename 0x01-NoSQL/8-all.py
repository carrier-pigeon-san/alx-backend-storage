#!/usr/bin/env python3
""" 8. List all documents in a MongoDB collection """
import pymongo


def list_all(mongo_collection):
    """ list all documents in a collection """
    return mongo_collection.find()
