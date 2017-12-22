#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

import os


# -------------------------------------------------------------------------


def path_to_dirs(path, remove_last=True):
    # split path to dir_str list, and remove last one(file name)
    path = os.path.normpath(path)
    ret = path.split(os.sep)

    if remove_last:
        ret.pop()  # remove file name, only leave dir part

    return ret

# -------------------------------------------------------------------------
