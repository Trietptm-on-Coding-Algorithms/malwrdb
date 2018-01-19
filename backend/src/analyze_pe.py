# -*- coding: utf-8 -*-
# !/usr/bin/python3

"""Analyze PE32 stuff."""

# -------------------------------------------------------------------------

import pprint
from datetime import datetime

from celery.utils.log import get_task_logger

from utils import to_str
from models_task import TaskStage
from models_pe import PeDosHeader, PeFileHeader, PeNtHeader, set_pe_value_list_by_dict, \
    PeSection, PeImportDllItem, PeImportDllTable


logger = get_task_logger(__name__)

# -------------------------------------------------------------------------


def analyze_pe_header(celery_task_id, pe, sample_tmp_id, stage_num):
    """Analyze pe header, and some db stuff."""
    stage_db = TaskStage()
    stage_db.celery_task_id = celery_task_id
    stage_db.stage_num = stage_num
    stage_db.stage_name = "analyze pe header"
    stage_db.save()

    try:
        # dos_header

        dos_header = pe.DOS_HEADER.dump_dict()
        dos_header.pop("Structure")

        dos_header_db = PeDosHeader()
        dos_header_db.sample_id = sample_tmp_id
        dos_header_db = set_pe_value_list_by_dict(dos_header_db, dos_header)
        dos_header_db.save()

        # file_header

        file_header = pe.FILE_HEADER.dump_dict()
        file_header.pop("Structure")

        file_header_db = PeFileHeader()
        file_header_db.sample_id = sample_tmp_id
        file_header_db = set_pe_value_list_by_dict(file_header_db, file_header)
        file_header_db.save()

        # nt_header

        nt_header = pe.NT_HEADERS.dump_dict()
        nt_header.pop("Structure")

        nt_header_db = PeNtHeader()
        nt_header_db.sample_id = sample_tmp_id
        nt_header_db = set_pe_value_list_by_dict(nt_header_db, nt_header)
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


def analyze_pe_sections(celery_task_id, pe, sample_tmp_id, stage_num):
    """Analyze pe section."""
    stage_db = TaskStage()
    stage_db.celery_task_id = celery_task_id
    stage_db.stage_num = stage_num
    stage_db.stage_name = "analyze pe sections"
    stage_db.save()

    try:
        # sections

        for section in pe.sections:

            section = section.dump_dict()
            section.pop("Structure")

            section_db = PeSection()
            section_db.sample_id = sample_tmp_id
            section_db = set_pe_value_list_by_dict(section_db, section)
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
        pe.parse_data_directories([0])
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):

            for import_dll in pe.DIRECTORY_ENTRY_IMPORT:

                import_dll_db = PeImportDllTable()
                import_dll_db.sample_id = sample_tmp_id
                import_dll_db.dll_name = to_str(import_dll.dll)

                struct = import_dll.struct.dump_dict()
                struct.pop("Structure")
                import_dll_db = set_pe_value_list_by_dict(import_dll_db, struct)

                # import_dll_db.import_item_list = []

                for import_item in import_dll.imports:

                    import_item_db = PeImportDllItem()
                    import_item_db.name = to_str(import_item.name)
                    import_item_db.ordinal = import_item.ordinal
                    import_item_db.bound = import_item.bound

                    if import_item.name:
                        import_dll_db.import_item_list.append(import_item_db)
                    else:
                        logger.error("import item has none name for dll %s" % import_dll.dll)

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


def analyze_pe_export_table(celery_task_id, pe, sample_tmp_id, stage_num):
    """Analyze pe import table."""
    stage_db = TaskStage()
    stage_db.celery_task_id = celery_task_id
    stage_db.stage_num = stage_num
    stage_db.stage_name = "analyze pe export table"
    stage_db.save()

    try:
        pe.parse_data_directories()

        if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):

            logger.error(pprint.pformat(pe.DIRECTORY_ENTRY_EXPORT))

            stage_db.finish_status = "success"

        else:

            logger.error("no export table parsed!")
            stage_db.finish_status = "no export table parsed!"

        # stage

        stage_db.finish_time = datetime.now()
        stage_db.save()

    except:
        PeImportDllTable.objects(sample_id=sample_tmp_id).delete()

        stage_db.finish_time = datetime.now()
        stage_db.finish_status = "fail!"
        stage_db.save()

        raise Exception("analyze pe export table")

# -------------------------------------------------------------------------
