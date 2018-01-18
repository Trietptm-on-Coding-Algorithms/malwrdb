# !/usr/bin/python3
# -*- coding: utf-8 -*-


"""Task definitions."""


# -------------------------------------------------------------------------


import traceback

import pefile
from celery.utils.log import get_task_logger

from tasks import app_celery
from tasks_util import connect_mongo
from defines import TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE
from models import RefFile, Sample
from analyze_pe import analyze_pe_header, analyze_pe_sections, analyze_pe_import_table, analyze_pe_export_table

logger = get_task_logger(__name__)

# -------------------------------------------------------------------------


@app_celery.task(name=TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE, bind=True)
def task_analyze_ref_file_as_sample(self, ref_file_id):
    """Analyze refFile as Sample.

    Every requirement is checked and passed.
    """
    celery_task_id = self.request.id

    # -2. connect to mongodb

    c = connect_mongo()

    # -1. check

    # only 1 RefFile
    q_file = RefFile.objects(pk=ref_file_id)
    if q_file.count() != 1:
        raise Exception("0 or more than 1 RefFile by ref_file_id: %d - %s" % (q_file.count(), ref_file_id))
    file = q_file[0]

    # 0. prepare stuff

    pe = pefile.PE(data=file._binary)

    try:

        sample_tmp = Sample()
        sample_tmp._binary = file._binary
        sample_tmp.save()
        sample_tmp_id = str(sample_tmp.pk)

        # pe header
        stage_num = 1
        analyze_pe_header(celery_task_id, pe, sample_tmp_id, stage_num)

        # pe sections
        stage_num += 1
        analyze_pe_sections(celery_task_id, pe, sample_tmp_id, stage_num)

        # import table
        stage_num += 1
        analyze_pe_import_table(celery_task_id, pe, sample_tmp_id, stage_num)

        # export table

        stage_num += 1
        analyze_pe_export_table(celery_task_id, pe, sample_tmp_id, stage_num)

        # x. del original RefFile and update some relationship
        # todo...

    except:
        # clean it up
        # sample_tmp.delete()

        logger.error("analze pe fail:")
        logger.error(traceback.format_exc())

    finally:

        sample_tmp.delete()

        # close mongodb connection
        c.close()

    logger.info("analze pe finish: %s" % ref_file_id)


# -------------------------------------------------------------------------
