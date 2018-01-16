# !/usr/bin/python3
# -*- coding: utf-8 -*-


"""Task definitions."""


# -------------------------------------------------------------------------


from tasks import app_celery
from defines import TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE

# -------------------------------------------------------------------------


@app_celery.task(name=TASK_TYPE_ANALYZE_REFFILE_AS_SAMPLE, bind=True)
def task_analyze_ref_file_as_sample(self, ref_file_id):
    """Analyze refFile as Sample.

    Every requirement is checked and passed.
    """
    celery_task_id = self.request.id
    print("analyze success %s" % ref_file_id)


# -------------------------------------------------------------------------
