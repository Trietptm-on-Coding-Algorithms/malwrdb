#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

import os


# -------------------------------------------------------------------------

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value

def path_to_dirs(path, remove_last=True):
    # split path to dir_str list, and remove last one(file name)
    path = os.path.normpath(path)
    ret = path.split(os.sep)

    if remove_last:
        ret.pop()  # remove file name, only leave dir part

    return ret

# -------------------------------------------------------------------------
