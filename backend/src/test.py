# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Test stuff."""

# -------------------------------------------------------------------------

from models import Sample
from tasks import sample_check_exist_or_insert

# -------------------------------------------------------------------------


def connect():
    """Connect to mongodb."""
    from flask_mongoengine import mongoengine
    return mongoengine.connect(db="malwrdb", host='127.0.0.1', port=27017, username="lyclovechl", password="yGeIgWof97zXrzayOwcIhIaF5EqcUR", authentication_source="admin")


def add_sample(file_path, encoding='utf-8'):
    """Add test sample to mongodb."""
    with open(file_path, mode='r', encoding=encoding) as f:
        sample_check_exist_or_insert(f.read())


def get_sample(id_):
    """Get sample from mongodb."""
    q = Sample.objects(pk=id_)
    if q.count() == 1:
        return q[0]
    else:
        print("invalid sample count: %d" % q.count())


# -------------------------------------------------------------------------


if __name__ == "__main__":
    # c = connect()

    # add_sample("/home/lovechl/code/malwrdb/test_samples/x.txt")
    # add_sample("/home/lovechl/code/malwrdb/test_samples/命令.exe", encoding='latin1')
    # add_sample("/home/lovechl/code/malwrdb/test_samples/c-免费版/c-免费版.exe", encoding='latin1')

    # sample = get_sample("5a30be401d41c8093c25d0d1")
    # print(sample.name)

    # c.close()
    pass


# -------------------------------------------------------------------------
