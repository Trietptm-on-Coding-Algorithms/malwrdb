# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Analyze PE32 stuff."""

# -------------------------------------------------------------------------

import pprint
from datetime import datetime

from celery.utils.log import get_task_logger

from utils import to_str
from models_task import TaskStage
from models_pe import PeDosHeader, PeFileHeader, PeNtHeader, PeValueStructureWithOffset, \
    PeValueStructureBase, PeSection, PeImportDllItem, PeImportDllTable


logger = get_task_logger(__name__)

# -------------------------------------------------------------------------


def set_pe_value_list_by_dict__with_offset(db_doc, dict_):
    """Tricky."""
    for k, v in dict_.items():
        value = PeValueStructureWithOffset()
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


def set_pe_value_list_by_dict__base(db_doc, dict_):
    """Tricky."""
    for k, v in dict_.items():
        value = PeValueStructureBase()
        value.name = k
        value.value_type = v.__class__.__name__
        if value.value_type == "str":
            value.value_str = v
        elif value.value_type == "int":
            value.value_int = v
        else:
            raise Exception("not supported value type!")
        db_doc.character_value_list.append(value)
    return db_doc


# -------------------------------------------------------------------------


def _retrieve_pe_header(pe):
    """Analyze PE header."""
    dos_header = pe.DOS_HEADER.dump_dict()
    dos_header.pop("Structure")

    file_header = pe.FILE_HEADER.dump_dict()
    file_header.pop("Structure")
    optional_header = pe.OPTIONAL_HEADER.dump_dict()
    optional_header.pop("Structure")
    optional_header["_data_directories"] = {}  # 为下面的 DataDirectories 准备
    nt_header = pe.NT_HEADERS.dump_dict()
    nt_header.pop("Structure")

    return (dos_header, file_header, nt_header)


def analyze_pe_header(celery_task_id, pe, sample_tmp_id, stage_num):
    """Analyze pe header, and some db stuff."""
    stage_db = TaskStage()
    stage_db.celery_task_id = celery_task_id
    stage_db.stage_num = stage_num
    stage_db.stage_name = "analyze pe header"
    stage_db.save()

    try:
        # retrieve and save to db

        dos_header, file_header, nt_header = _retrieve_pe_header(pe)

        # dos_header
        dos_header_db = PeDosHeader()
        dos_header_db.sample_id = sample_tmp_id
        dos_header_db = set_pe_value_list_by_dict__with_offset(dos_header_db, dos_header)
        dos_header_db.save()

        # file_header
        file_header_db = PeFileHeader()
        file_header_db.sample_id = sample_tmp_id
        file_header_db = set_pe_value_list_by_dict__with_offset(file_header_db, file_header)
        file_header_db.save()

        # nt_header
        nt_header_db = PeNtHeader()
        nt_header_db.sample_id = sample_tmp_id
        nt_header_db = set_pe_value_list_by_dict__with_offset(nt_header_db, nt_header)
        nt_header_db.save()

        # save stage to db

        stage_db.finish_time = datetime.now()
        stage_db.finish_status = "success"
        stage_db.save()

    except:
        # remove everything created!

        PeDosHeader.objects(sample_id=sample_tmp_id).delete()
        PeFileHeader.objects(sample_id=sample_tmp_id).delete()
        PeNtHeader.objects(sample_id=sample_tmp_id).delete()

        # save stage to db

        stage_db.finish_time = datetime.now()
        stage_db.finish_status = "fail!"
        stage_db.save()

        raise Exception("analyze pe hader fail")


def _retrieve_pe_sections(pe):
    """Retrieve pe sections info from pe."""
    ret = []
    for section in pe.sections:

        # 获取

        pe_section = section.dump_dict()
        pe_section.pop("Structure")
        pe_section_ = {}
        for (k, v) in pe_section.items():
            pe_section_[k] = v["Value"]

        ret.append(pe_section_)

    return ret


def analyze_pe_sections(celery_task_id, pe, sample_tmp_id, stage_num):
    """Analyze pe section."""
    stage_db = TaskStage()
    stage_db.celery_task_id = celery_task_id
    stage_db.stage_num = stage_num
    stage_db.stage_name = "analyze pe sections"
    stage_db.save()

    try:
        # retrieve sections from pe

        section_list = _retrieve_pe_sections(pe)

        # logger.info(pprint.pformat(section_list))

        # sections

        for section in section_list:
            section_db = PeSection()
            section_db.sample_id = sample_tmp_id
            section_db = set_pe_value_list_by_dict__base(section_db, section)
            section_db.save()

        # stage

        stage_db.finish_time = datetime.now()
        stage_db.finish_status = "success"
        stage_db.save()

    except:
        PeSection.objects(sample_id=sample_tmp_id).delete()

        stage_db.finish_time = datetime.now()
        stage_db.finish_status = "fail!"
        stage_db.save()

        raise Exception("analyze pe sections fail")


def analyze_pe_import_table(celery_task_id, pe, sample_tmp_id, stage_num):
    """Analyze pe import table."""
    stage_db = TaskStage()
    stage_db.celery_task_id = celery_task_id
    stage_db.stage_num = stage_num
    stage_db.stage_name = "analyze pe import table"
    stage_db.save()

    try:
        # retrieve sections from pe

        pe.parse_data_directories([0])
        import_table = pe.DIRECTORY_ENTRY_IMPORT

        if import_table:

            # import table

            for import_dll in import_table:

                import_dll_db = PeImportDllTable()
                import_dll_db.sample_id = sample_tmp_id
                import_dll_db.dll_name = to_str(import_dll.dll)

                struct = import_dll.struct.dump_dict()
                struct.pop("Structure")
                import_dll_db = set_pe_value_list_by_dict__with_offset(import_dll_db, struct)

                for import_item in import_dll.imports:

                    import_item_db = PeImportDllItem()
                    import_item_db.name = import_item.name
                    import_item_db.ordinal = import_item.ordinal
                    import_item_db.bound = import_item.bound

                    logger.info(pprint.pformat(import_item_db))

                import_dll_db.save()

            stage_db.finish_status = "success"

        else:

            stage_db.finish_status = "no import table parsed!"

        # stage

        stage_db.finish_time = datetime.now()
        stage_db.save()

    except:
        PeImportDllTable.objects(sample_id=sample_tmp_id).delete()

        stage_db.finish_time = datetime.now()
        stage_db.finish_status = "fail!"
        stage_db.save()

        raise Exception("analyze pe import table")


# -------------------------------------------------------------------------
