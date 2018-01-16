# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Mongodb Document definitions."""

# -------------------------------------------------------------------------

import json
import hashlib
from datetime import datetime

from flask_mongoengine import mongoengine


# -------------------------------------------------------------------------


class LogLine(mongoengine.Document):
    """Log stuff."""

    meta = {'collection': "log_line"}

    file = mongoengine.StringField(required=True)
    level = mongoengine.StringField(required=True)
    info = mongoengine.StringField(required=True)

    add_time = mongoengine.DateTimeField(default=datetime.now())

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        del ret["_id"]

        return ret


# -------------------------------------------------------------------------


class RefGroup(mongoengine.Document):
    """A group of refFiles/dirs/samples."""

    meta = {'collection': "ref_group"}

    group_id = mongoengine.StringField(required=True)

    add_time = mongoengine.DateTimeField(default=datetime.now())
    update_time = mongoengine.DateTimeField()

    def clean(self):
        """Set update_time."""
        self.update_time = datetime.now()

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        del ret["_id"]
        del ret["add_time"]

        return ret


class RefDir(mongoengine.Document):
    """So we can orginaze files."""

    meta = {'collection': "ref_dir"}

    dir_name = mongoengine.StringField(required=True)

    refGroup = mongoengine.ReferenceField('RefGroup', required=True)
    parnetRefDir = mongoengine.ReferenceField('self')

    def clean(self):
        """Update  "update_time" of corresponding refGroup."""
        self.refGroup.save()  # update it's update_time

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        # # frontend need this _id as string
        ret["_id"] = str(self.pk)

        del ret["refGroup"]
        if "parnetRefDir" in ret:
            del ret["parnetRefDir"]

        return ret


class SampleBelongTo(mongoengine.Document):
    """Use this to decide "location" of a sample."""

    meta = {'collection': "sample_belongto"}

    refGroup = mongoengine.ReferenceField('RefGroup', required=True)
    refDir = mongoengine.ReferenceField('RefDir', required=True)

    sample_id = mongoengine.StringField(required=True)
    parent_sample_id = mongoengine.StringField()
    parent_sample_to_this_type = mongoengine.StringField()

    sample_name = mongoengine.StringField(required=True)
    sample_relative_path = mongoengine.StringField()

    def clean(self):
        """Update "update_time" of corresponding refGroup."""
        self.refGroup.save()  # update it's update_time


class Sample(mongoengine.Document):
    """Sample.

    Only "solid" information here.
    """

    meta = {'collection': "sample"}

    _binary = mongoengine.BinaryField()

    md5 = mongoengine.StringField(max_length=32, min_length=32)
    sha1 = mongoengine.StringField(max_length=40, min_length=40)
    sha256 = mongoengine.StringField(max_length=64, min_length=64)
    sha512 = mongoengine.StringField(max_length=128, min_length=128)

    sample_size = mongoengine.IntField()
    sample_file_type = mongoengine.StringField()

    ssdeep = mongoengine.StringField()
    imphash = mongoengine.StringField()
    crc32 = mongoengine.StringField()

    platform = mongoengine.StringField()
    is_malicious = mongoengine.BooleanField()
    malware_name_list = mongoengine.ListField()
    malware_family_list = mongoengine.ListField()

    analyze_time = mongoengine.DateTimeField()

    update_time = mongoengine.DateTimeField()

    def clean(self):
        """Update some."""
        pass

    def to_filter(self):
        """What?."""
        return {"sha256": self.sha256}

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        del ret["_id"]
        assert "_binary" in ret
        del ret["_binary"]
        return ret


class RefFileBelongTo(mongoengine.Document):
    """Use this to decide "location" of a refFile."""

    meta = {'collection': "ref_file_belongto"}

    refGroup = mongoengine.ReferenceField('RefGroup', required=True)
    refDir = mongoengine.ReferenceField('RefDir', required=True)

    ref_file_id = mongoengine.StringField(required=True)

    file_name = mongoengine.StringField(required=True)
    file_relative_path = mongoengine.StringField()

    def clean(self):
        """Update "update_time" of corresponding regGroup."""
        self.refGroup.save()  # update it's update_time


class RefFile(mongoengine.Document):
    """File for Reference."""

    meta = {'collection': "ref_file"}

    _binary = mongoengine.BinaryField()

    md5 = mongoengine.StringField(max_length=32, min_length=32)
    sha1 = mongoengine.StringField(max_length=40, min_length=40)
    sha256 = mongoengine.StringField(max_length=64, min_length=64)
    sha512 = mongoengine.StringField(max_length=128, min_length=128)

    file_size = mongoengine.IntField()
    file_type = mongoengine.StringField()

    def clean(self):
        """Update some thing on save."""
        if self._binary and len(self._binary) != 0:

            self.file_size = len(self._binary)
            self.md5 = hashlib.md5(self._binary).hexdigest()
            self.sha1 = hashlib.sha1(self._binary).hexdigest()
            self.sha256 = hashlib.sha256(self._binary).hexdigest()
            self.sha512 = hashlib.sha512(self._binary).hexdigest()
        else:
            self.file_size = 0

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        ret["_id"] = str(self.pk)
        if "_binary" in ret:
            del ret["_binary"]

        return ret


# -------------------------------------------------------------------------


class TaskStage(mongoengine.Document):
    """Task stage."""

    meta = {'collection': 'task_history'}

    celery_task_id = mongoengine.StringField(required=True)
    stage_num = mongoengine.IntField(required=True)
    stage_name = mongoengine.StringField(required=True)

    start_time = mongoengine.DateTimeField(required=True)  # equal to create_time
    latest_status = mongoengine.StringField(required=True)

    finish_time = mongoengine.DateTimeField()
    finish_status = mongoengine.StringField()

    add_time = mongoengine.DateTimeField(default=datetime.now())
    update_time = mongoengine.DateTimeField()

    def clean(self):
        """When save, set self.update_time."""
        self.update_time = datetime.now()

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

    add_time = mongoengine.DateTimeField(default=datetime.now())
    update_time = mongoengine.DateTimeField()

    def clean(self):
        """When save, set self.update_time."""
        self.update_time = datetime.now()

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        ret["_id"] = str(self.pk)

        ret["create_time"] = ret["create_time"]["$date"]
        if "finish_time" in ret:
            ret["finish_time"] = ret["finish_time"]["$date"]

        return ret


# -------------------------------------------------------------------------
