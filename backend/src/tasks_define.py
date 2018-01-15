# !/usr/bin/python3
# -*- coding: utf-8 -*-


"""Task definitions."""


# -------------------------------------------------------------------------


from tasks import app_celery


# -------------------------------------------------------------------------


@app_celery.task(name="analyze_ref_file_as_sample")
def task_analyze_ref_file_as_sample(ref_file_id):
    """Analyze refFile as Sample.

    Every requirement is checked and passed.
    """
    while True:
        print("analyzing %s" % ref_file_id)
        import time
        time.sleep(3)


# -------------------------------------------------------------------------
