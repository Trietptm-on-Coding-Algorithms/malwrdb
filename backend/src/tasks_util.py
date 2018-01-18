# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Analyze PE32 stuff."""

# -------------------------------------------------------------------------


from flask_mongoengine import mongoengine


# -------------------------------------------------------------------------


def connect_mongo():
    """Connect to mongodb.

    Because Celery schedule tasks in seperate process, so we need to connect to mongo there.
    """
    return mongoengine.connect("malwrdb", host="127.0.0.1", port=27019, username="lyclovechl", password="yGeIgWof97zXrzayOwcIhIaF5EqcUR", authentication_source="admin")


# -------------------------------------------------------------------------
