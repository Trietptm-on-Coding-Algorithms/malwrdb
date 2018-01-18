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

    add_time = mongoengine.DateTimeField(default=datetime.now())
    update_time = mongoengine.DateTimeField()

    def clean(self):
        """Update self.update_time."""
        self.update_time = datetime.now()

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

    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

    ordinal = mongoengine.IntField(required=True)
    name = mongoengine.StringField(required=True)
    bound = mongoengine.StringField()


class PeImportDllTable(PeBaseDocument):
    """Pe Import table."""

    meta = {'collection': "pe_import_table"}

    dll_name = mongoengine.StringField(required=True)
    import_item_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PeImportDllItem))
    character_value_list = mongoengine.ListField(mongoengine.EmbeddedDocumentField(PeValueStructure))


# -------------------------------------------------------------------------


def clear_pe_documents():
    """Drop all collection defined here."""
    PeDosHeader.drop_collection()
    PeFileHeader.drop_collection()
    PeNtHeader.drop_collection()
    PeSection.drop_collection()
    PeImportDllTable.drop_collection()


# -------------------------------------------------------------------------
