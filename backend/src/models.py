# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Mongodb Document definitions - basic stuff."""

# -------------------------------------------------------------------------

import json
import hashlib
from datetime import datetime

from flask_mongoengine import mongoengine


# -------------------------------------------------------------------------


class RefGroup(mongoengine.Document):
    """A group of refFiles/dirs/samples."""

    meta = {'collection': "ref_group"}

    group_id = mongoengine.StringField(required=True)   # random gened string

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

    # automatically updated in self.save()
    sample_size = mongoengine.IntField()
    md5 = mongoengine.StringField(max_length=32, min_length=32)
    sha1 = mongoengine.StringField(max_length=40, min_length=40)
    sha256 = mongoengine.StringField(max_length=64, min_length=64)
    sha512 = mongoengine.StringField(max_length=128, min_length=128)

    sample_file_type = mongoengine.StringField()

    ssdeep = mongoengine.StringField()
    imphash = mongoengine.StringField()
    crc32 = mongoengine.StringField()

    platform = mongoengine.StringField()
    is_malicious = mongoengine.BooleanField()
    malware_name_list = mongoengine.ListField()
    malware_family_list = mongoengine.ListField()

    analyze_time = mongoengine.DateTimeField()
    add_time = mongoengine.DateTimeField(default=datetime.now())
    update_time = mongoengine.DateTimeField()

    def clean(self):
        """Update some."""
        if self._binary and len(self._binary) != 0:

            self.sample_size = len(self._binary)
            self.md5 = hashlib.md5(self._binary).hexdigest()
            self.sha1 = hashlib.sha1(self._binary).hexdigest()
            self.sha256 = hashlib.sha256(self._binary).hexdigest()
            self.sha512 = hashlib.sha512(self._binary).hexdigest()
        else:
            self.sample_size = 0

        self.update_time = datetime.now()

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


def clear_documents():
    """Drop collections defined here."""
    RefGroup.drop_collection()
    RefDir.drop_collection()
    SampleBelongTo.drop_collection()
    Sample.drop_collection()
    RefFileBelongTo.drop_collection()
    RefFile.drop_collection()


def recur_del_ref_dir(ref_dir):
    """Del refDir and it's sub contents recurly."""
    # sub dir
    for sub_dir in RefDir.objects(parnetRefDir=ref_dir):
        recur_del_ref_dir(sub_dir)

    # sub file
    for file_belong_to in RefFileBelongTo.objects(refDir=ref_dir):
        if RefFileBelongTo.objects(ref_file_id=file_belong_to.pk).count() == 1:

            # this file belong to this dir "only", so we need del it

            q_file = RefFile.objects(pk=file_belong_to.ref_file_id)
            if q_file.count() != 1:
                raise Exception("e...this is embarssing, 0 or more than 1 ref file")

            q_file.delete()

    RefFileBelongTo.objects(refDir=ref_dir).delete()

    # sub sample
    for sample_belong_to in SampleBelongTo.objects(refDir=ref_dir):
        if SampleBelongTo.objects(sample_id=sample_belong_to.sample_id).count() == 1:

            # this sample belong to this dir "only", so we need del it

            q_sample = Sample.objects(pk=sample_belong_to.sample_id)
            if q_sample.count() != 1:
                raise Exception("e...this is embarssing, 0 or more than 1 sample")

    SampleBelongTo.objects(refDir=ref_dir).delete()

    # if dir is topDir, delete RefGroup also
    if "parnetRefDir" not in ref_dir:
        if RefDir.objects(refGroup=ref_dir.refGroup).count() != 1:
            raise Exception("suspecious topDir, no parnetRefDir, but 0 or more than 1 refDir with same RefGroup")
        ref_dir.refGroup.delete()

    # self del
    ref_dir.delete()


# -------------------------------------------------------------------------
