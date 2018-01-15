# !/usr/bin/python3
# -*- coding: utf-8 -*-


"""Task definitions."""


# -------------------------------------------------------------------------


from tasks import app_celery
from defines import TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE

# -------------------------------------------------------------------------


@app_celery.task(name=TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE)
def task_analyze_ref_file_as_sample(ref_file_id):
    """Analyze refFile as Sample.

    Every requirement is checked and passed.
    """
    while True:
        print("analyzing %s" % ref_file_id)
        import time
        time.sleep(3)


# -------------------------------------------------------------------------
