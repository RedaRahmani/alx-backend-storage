#!/usr/bin/env python3
"""  Inserts a new document in a collection based on kwargs """


def insert_school(mongo_collection, **kwargs):
    """ inserts a new document based on kwargs
    and returns the new id
    """
    return mongo_collection.insert(kwargs)
