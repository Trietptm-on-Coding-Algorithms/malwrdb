# !/usr/bin/python3
# -*- coding: utf-8 -*-


"""Task wrapper functions."""

# -------------------------------------------------------------------------

import time
from datetime import datetime

from models import RefFile, TaskHistory
from tasks import get_active_task_list
from tasks_define import task_analyze_ref_file_as_sample


# -------------------------------------------------------------------------

# task info


def get_task_info():
    """Get and format task info from tasks.py then return to ui."""
    ret = []
    for task in get_active_task_list():
        ret.append(task)
    return ret


# -------------------------------------------------------------------------

# task history


def get_task_history():
    """Get all TaskHistory from mongodb."""
    ret = []
    for history in TaskHistory.objects.order_by("-add_time"):
        ret.append(history.json_ui())
    return ret


def get_task_history_not_closed():
    """Get TaskHistroy in mongodb that not 'closed'."""
    return TaskHistory.objects(finish_time=None)


# -------------------------------------------------------------------------


def analyze_ref_file_as_sample(ref_file_id):
    """Check requirments, and add task to worker if everything ok.

    - For now, we only support PE32.
    - This shall be singleton.
    """
    from defines import TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE

    # 1. check params

    q_ref_file = RefFile.objects(pk=ref_file_id)
    if q_ref_file.count() != 1:
        raise Exception("0 or more than 1 refFile by id: %s" % ref_file_id)

    # 2. check if alreay has running/pending tasks

    q_analyze_task = get_task_history_not_closed().filter(task_type=TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE, ref_file_id=ref_file_id)
    if q_analyze_task.count() != 0:
        raise Exception("task of analyzing this ref file as sample is running, don't start another!")

    # x. everything checked! add to celery worker and mongodb TaskHistory
    task_history = TaskHistory()
    task_history.task_type = TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE
    task_history.ref_file_id = ref_file_id
    task_history.start_time = datetime.now()
    task_history.analyze_type = "PE32"
    task_history.celery_task_id = task_analyze_ref_file_as_sample.delay(ref_file_id)
    task_history.latest_status = "added_to_celery_worker"
    task_history.save()


# -------------------------------------------------------------------------


def check_close_task_history():
    """Some TaskHistory in mongodb might not "properly" 'closed', we need to check this.

    - Run this in a single thread.
    """
    from tasks import check_has_not_finished_task
    while True:
        for history in get_task_history_not_closed():
            if not check_has_not_finished_task(history.celery_task_id):
                history.finish_time = datetime.now()
                history.finish_status = "force close"
                history.save()
        time.sleep(5)


# -------------------------------------------------------------------------
