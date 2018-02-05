# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Mongodb Document definitions - Task stuff."""

# -------------------------------------------------------------------------

import json
from datetime import datetime

from flask_mongoengine import mongoengine


# -------------------------------------------------------------------------


class TaskStage(mongoengine.Document):
    """Task stage."""

    meta = {'collection': 'task_stage'}

    celery_task_id = mongoengine.StringField(required=True)
    stage_num = mongoengine.IntField(required=True)
    stage_name = mongoengine.StringField(required=True)

    start_time = mongoengine.DateTimeField(default=datetime.now(tz=None))  # equal to create_time, and almost same with add_time
    finish_time = mongoengine.DateTimeField()
    finish_status = mongoengine.StringField()

    add_time = mongoengine.DateTimeField(default=datetime.now(tz=None))
    update_time = mongoengine.DateTimeField()

    def clean(self):
        """When save, set self.update_time."""
        self.update_time = datetime.now(tz=None)

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        ret["_id"] = str(self.pk)

        ret["create_time"] = ret["create_time"]["$date"]
        if "finish_time" in ret:
            ret["finish_time"] = ret["finish_time"]["$date"]

        return ret


class TaskHistory(mongoengine.Document):
    """Task history."""

    meta = {'collection': 'task_history'}

    celery_task_id = mongoengine.StringField(required=True)
    task_type = mongoengine.StringField(required=True)
    create_time = mongoengine.DateTimeField(required=True)
    latest_status = mongoengine.StringField(required=True)

    start_time = mongoengine.DateTimeField()
    finish_time = mongoengine.DateTimeField()
    finish_status = mongoengine.StringField()

    # task_type: analyze_refFile_as_sample
    ref_file_id = mongoengine.StringField()    # if analyze success, this will be set as none
    sample_id = mongoengine.StringField()      # if anlyaze fail, this will not set
    analyze_type = mongoengine.StringField()   #
    fail_reason = mongoengine.StringField()    # if analyze fail, this describe why

    # task_type: compare samples to find similarity
    # ...

    add_time = mongoengine.DateTimeField(default=datetime.now(tz=None))
    update_time = mongoengine.DateTimeField()

    def clean(self):
        """When save, set self.update_time."""
        self.update_time = datetime.now(tz=None)

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        ret["_id"] = str(self.pk)

        ret["create_time"] = ret["create_time"]["$date"]
        if "finish_time" in ret:
            ret["finish_time"] = ret["finish_time"]["$date"]

        return ret


# -------------------------------------------------------------------------
