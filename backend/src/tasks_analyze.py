# !/usr/bin/python3
# -*- coding: utf-8 -*-


"""Task analyze methods."""


# -------------------------------------------------------------------------


from datetime import datetime

from models import RefFileBelongTo, SampleBelongTo
from models_task import TaskStage


# -------------------------------------------------------------------------


def replace_ref_file_by_sample(celery_task_id, sample_tmp_id, stage_num, ref_file):
    """Let Sample has same relationship with RefFile, then Delete RefFile and it's relationships."""
    # inherit all relationships
    for file_belong_to in RefFileBelongTo.objects(ref_file_id=ref_file.pk):

        stage_num += 1
        stage_db = TaskStage()
        stage_db.celery_task_id = celery_task_id
        stage_db.stage_num = stage_num
        stage_db.stage_name = "Let Sample has same relationship with RefFile"
        stage_db.save()

        try:

            # inherit

            sample_belong_to = SampleBelongTo()
            sample_belong_to.sample_id = sample_tmp_id
            sample_belong_to.refGroup = file_belong_to.refGroup
            sample_belong_to.refDir = file_belong_to.refDir
            sample_belong_to.sample_name = file_belong_to.file_name
            if "file_relative_path" in file_belong_to:
                sample_belong_to.sample_relative_path = file_belong_to.file_relative_path
            sample_belong_to.save()

            stage_db.finish_time = datetime.now()
            stage_db.finish_status = "success"
            stage_db.save()

        except:
            # save stage to db

            stage_db.finish_time = datetime.now()
            stage_db.finish_status = "fail!"
            stage_db.save()

            raise Exception("Let Sample has same relationship with RefFile failed!")

    # Delete RefFile and all relationships

    stage_num += 1
    stage_db = TaskStage()
    stage_db.celery_task_id = celery_task_id
    stage_db.stage_num = stage_num
    stage_db.stage_name = "Delete RefFile and all relationships"
    stage_db.save()

    try:

        ref_file.delete()
        RefFileBelongTo.objects(ref_file_id=ref_file.pk).delete()

        stage_db.finish_time = datetime.now()
        stage_db.finish_status = "success"
        stage_db.save()

    except:
        stage_db.finish_time = datetime.now()
        stage_db.finish_status = "fail!"
        stage_db.save()

        raise Exception("Let Sample has same relationship with RefFile failed!")


# -------------------------------------------------------------------------
