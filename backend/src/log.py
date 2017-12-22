#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

from models import *

# -------------------------------------------------------------------------


def log(file, info, level):
    # print log to screen and save to database
    print("[%s] : %s" % (level.upper(), info))

    try:
        log_ = LogLine()
        log_.file = file
        log_.info = info
        log_.level = level.upper()
        log_.save()
    except:
        pass


# -------------------------------------------------------------------------