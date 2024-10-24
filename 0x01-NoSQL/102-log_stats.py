#!/usr/bin/env python3
""" A script that provides some stats about Nginx logs stored in MongoDB """
import pymongo
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient(host='localhost', port=27017)
    db = client.logs
    col = db.nginx

    print(f"{col.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print(f"\tmethod {method}: {col.count_documents({'method': method})}")
    print("{} status check".format(
        col.count_documents({'method': 'GET', 'path': '/status'})
        ))
    print("IPs:")
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "total_ips": {"$sum": 1}
            }
        },
        {"$sort": {"total_ips": -1}},
        {
            "$limit": 10
        }
    ]
    for ip in col.aggregate(pipeline):
        print("\t{}: {}".format(ip['_id'], ip['total_ips']))
