#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

import json
import hashlib
from datetime import datetime

from flask_mongoengine import mongoengine

# -------------------------------------------------------------------------

class LogLine(mongoengine.Document):
    """
    日志
    """
    meta = {'collection': "log_line"}

    file = mongoengine.StringField(required=True)
    level = mongoengine.StringField(required=True)
    info = mongoengine.StringField(required=True)

    add_time = mongoengine.DateTimeField(default=datetime.now())

    def json_ui(self):
        ret = json.loads(self.to_json())

        del ret["_id"]

        return ret


class RefGroup(mongoengine.Document):
    """
    a group of refFiles/dirs/samples
    """
    meta = {'collection': "ref_group"}

    group_id = mongoengine.StringField(required=True)

    add_time = mongoengine.DateTimeField(default=datetime.now())
    update_time = mongoengine.DateTimeField()

    def clean(self):
        self.update_time = datetime.now()

    def json_ui(self):
        ret = json.loads(self.to_json())

        del ret["_id"]
        del ret["add_time"]

        return ret


class RefDir(mongoengine.Document):
    """
    so we can orginaze files
    """
    meta = {'collection': "ref_dir"}

    dir_name = mongoengine.StringField(required=True)

    refGroup = mongoengine.ReferenceField('RefGroup', required=True)
    parnetRefDir = mongoengine.ReferenceField('self')

    def clean(self):
        self.refGroup.save()  # update it's update_time

    def json_ui(self):
        ret = json.loads(self.to_json())

        # # frontend need this _id as string
        ret["_id"] = str(self.pk)

        del ret["refGroup"]
        if "parnetRefDir" in ret:
            del ret["parnetRefDir"]

        return ret


class SampleBelongTo(mongoengine.Document):
    """
    use this to decide "location" of a sample
    """
    meta = {'collection': "sample_belongto"}

    refGroup = mongoengine.ReferenceField('RefGroup', required=True)
    refDir = mongoengine.ReferenceField('RefDir', required=True)

    sample_id = mongoengine.StringField(required=True)
    parent_sample_id = mongoengine.StringField()
    parent_sample_to_this_type = mongoengine.StringField()

    sample_name = mongoengine.StringField(required=True)
    sample_relative_path = mongoengine.StringField()

    def clean(self):
        self.refGroup.save()  # update it's update_time


class Sample(mongoengine.Document):
    """
    sample. only "solid" information
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
        pass

    def to_filter(self):
        return {"sha256": self.sha256}

    def json_ui(self):
        """返回到界面的 Json"""
        ret = json.loads(self.to_json())

        del ret["_id"]
        assert "_binary" in ret
        del ret["_binary"]
        return ret


class RefFileBelongTo(mongoengine.Document):
    """
    use this to decide "location" of a refFile
    """
    meta = {'collection': "ref_file_belongto"}

    refGroup = mongoengine.ReferenceField('RefGroup', required=True)
    refDir = mongoengine.ReferenceField('RefDir', required=True)

    ref_file_id = mongoengine.StringField(required=True)

    file_name = mongoengine.StringField(required=True)
    file_relative_path = mongoengine.StringField()

    def clean(self):
        self.refGroup.save()  # update it's update_time


class RefFile(mongoengine.Document):
    """
    File for Reference
    """
    meta = {'collection': "ref_file"}

    _binary = mongoengine.BinaryField()

    md5 = mongoengine.StringField(max_length=32, min_length=32)
    sha1 = mongoengine.StringField(max_length=40, min_length=40)
    sha256 = mongoengine.StringField(max_length=64, min_length=64)
    sha512 = mongoengine.StringField(max_length=128, min_length=128)

    file_size = mongoengine.IntField()
    file_type = mongoengine.StringField()

    def clean(self):
        if self._binary and len(self._binary) != 0:

            self.file_size = len(self._binary)
            self.md5 = hashlib.md5(self._binary).hexdigest()
            self.sha1 = hashlib.sha1(self._binary).hexdigest()
            self.sha256 = hashlib.sha256(self._binary).hexdigest()
            self.sha512 = hashlib.sha512(self._binary).hexdigest()
        else:
            self.file_size = 0

    def json_ui(self):
        """返回到界面的 Json"""
        ret = json.loads(self.to_json())

        ret["_id"] = str(self.pk)
        if "_binary" in ret:
            del ret["_binary"]

        return ret

# -------------------------------------------------------------------------
