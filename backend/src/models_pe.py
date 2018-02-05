# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Mongodb Document definitions - log stuff."""

# -------------------------------------------------------------------------

import json
from datetime import datetime

from flask_mongoengine import mongoengine


# -------------------------------------------------------------------------

# base class


class PeBaseDocument(mongoengine.Document):
    """PE Dos header."""

    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    sample_id = mongoengine.StringField(required=True)

    add_time = mongoengine.DateTimeField(default=datetime.now(tz=None))
    update_time = mongoengine.DateTimeField()

    def clean(self):
        """Update self.update_time."""
        self.update_time = datetime.now(tz=None)

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        del ret["_id"]

        return ret


# -------------------------------------------------------------------------


class PeValueStructure(mongoengine.EmbeddedDocument):
    """Base of name->value structure."""

    name = mongoengine.StringField(required=True)
    value_type = mongoengine.StringField(required=True)
    offset_file = mongoengine.IntField(required=True)
    offset_mm = mongoengine.IntField(required=True)

    value_int = mongoengine.IntField()
    value_str = mongoengine.StringField()

    def clean(self):
        """Check self.value_type here."""
        if self.value_type not in ["int", "str"]:
            raise Exception("not supported self.value_type: %s" % self.value_type)

        if self.value_type == "int" and "value_int" not in self:
            raise Exception("no int value provided!")

        elif self.value_type == "str" and "value_str" not in self:
            raise Exception("no str value provided!")

        else:
            pass

    def value(self):
        """Get value by self.value_binary."""
        if self.value_type == "str":
            return self.value_str
        elif self.value_type == "int":
            return self.value_int
        else:
            raise Exception("invalid self.value_type!")

    def json_ui(self):
        """Json object return to UI."""
        ret = {}

        ret["name"] = self.name
        ret["offset_file"] = self.offset_file
        ret["offset_mm"] = self.offset_mm
        ret["value"] = self.value()

        return ret


class PeDosHeader(PeBaseDocument):
    """PE Dos header."""

    meta = {'collection': "pe_dos_header"}

    character_value_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PeValueStructure))


class PeFileHeader(PeBaseDocument):
    """PE File header."""

    meta = {'collection': "pe_file_header"}

    character_value_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PeValueStructure))


class PeNtHeader(PeBaseDocument):
    """PE Nt header."""

    meta = {'collection': "pe_nt_header"}

    character_value_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PeValueStructure))


class PeSection(PeBaseDocument):
    """PE segment."""

    meta = {'collection': "pe_section"}

    character_value_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PeValueStructure))


class PeImportDllItem(mongoengine.EmbeddedDocument):
    """Pe Import table item."""

    name = mongoengine.StringField(required=True)
    ordinal = mongoengine.IntField()
    bound = mongoengine.StringField()

    def json_ui(self):
        """Json object return to UI."""
        ret = json.loads(self.to_json())

        # no "_id" here, because no self.save() invoked!
        # del ret["_id"]

        return ret


class PeImportDllTable(PeBaseDocument):
    """Pe Import table."""

    meta = {'collection': "pe_import_table"}

    dll_name = mongoengine.StringField(required=True)
    import_item_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PeImportDllItem))
    character_value_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PeValueStructure))


# -------------------------------------------------------------------------


def clear_pe_documents(sample_id=None):
    """Drop all collection defined here, or that related with sample."""
    if not sample_id:
        PeDosHeader.drop_collection()
        PeFileHeader.drop_collection()
        PeNtHeader.drop_collection()
        PeSection.drop_collection()
        PeImportDllTable.drop_collection()
    else:
        PeDosHeader.objects(sample_id=sample_id).delete()
        PeFileHeader.objects(sample_id=sample_id).delete()
        PeNtHeader.objects(sample_id=sample_id).delete()
        PeSection.objects(sample_id=sample_id).delete()
        PeImportDllTable.objects(sample_id=sample_id).delete()


def set_pe_value_list_by_dict(db_doc, dict_):
    """Tricky."""
    for k, v in dict_.items():
        value = PeValueStructure()
        value.name = k
        value.offset_file = v["FileOffset"]
        value.offset_mm = v["Offset"]
        value.value_type = v["Value"].__class__.__name__
        if value.value_type == "str":
            value.value_str = v["Value"]
        elif value.value_type == "int":
            value.value_int = v["Value"]
        else:
            raise Exception("not supported value type!")
        db_doc.character_value_list.append(value)
    return db_doc


def get_pe_value_list(db_doc):
    """Tricky."""
    return sorted(db_doc.character_value_list, key=lambda v: v.offset_file)


def pe_value_list_to_dict(db_doc):
    """Convert pe value list to a pe value dict."""
    ret = {}
    for value_structure in db_doc.character_value_list:
        ret[value_structure.name] = value_structure.value()
    return ret

# -------------------------------------------------------------------------
