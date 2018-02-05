# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Mongodb Document definitions - log stuff."""

# -------------------------------------------------------------------------

import json
from datetime import datetime

from flask_mongoengine import mongoengine


# -------------------------------------------------------------------------


class LogLine(mongoengine.Document):
    """Log stuff."""

    meta = {'collection': "log_line"}

    file = mongoengine.StringField(required=True)
    level = mongoengine.StringField(required=True)
    info = mongoengine.StringField(required=True)

    add_time = mongoengine.DateTimeField(default=datetime.now(tz=None))

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        del ret["_id"]

        return ret


# -------------------------------------------------------------------------
