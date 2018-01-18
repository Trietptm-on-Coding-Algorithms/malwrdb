# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Log func definations."""


# -------------------------------------------------------------------------


from models_log import LogLine


# -------------------------------------------------------------------------


def log(file, info, level):
    """Print log to screen and save to database."""
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
