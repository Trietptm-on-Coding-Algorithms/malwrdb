# !/usr/bin/python3
# -*- coding: utf-8 -*-


"""Task helper functions.

To make this work, u need:
    1. start redis at port 6381
    2. start celery worker by execute in this file dir: celery -A tasks worker --loglevel=info
"""


# -------------------------------------------------------------------------


from celery import Celery

node_name = "celery@ubuntu"  # use default as the only node
app_celery = Celery('tasks', broker='redis://localhost:6381/9', include=['tasks_define'])
app_celery.conf.result_backend = 'redis://localhost:6381/10'


# -------------------------------------------------------------------------

# task info get


def _get_inspect():
    """Get inspect."""
    return app_celery.control.inspect([node_name])  # celery@host_name


def get_registered_task_name_list():
    """Get task name list from celery worker.

    @return: list : a list of task names.
    """
    i = _get_inspect()
    return i.registered()[node_name]


def get_reserved_task_list():
    """Get received but waiting to be executed task list."""
    i = _get_inspect()
    return i.reserved()


def get_scheduled_task_list():
    """Get not active but wating to be scheduled task list."""
    i = _get_inspect()
    return i.scheduled()


def get_active_task_list():
    """Get active task list.

    {'acknowledged': True,
    'args': '()',
    'delivery_info': {'exchange': '',
                      'priority': 0,
                      'redelivered': None,
                      'routing_key': 'celery'},
    'hostname': 'celery@ubuntu',
    'id': '8d1ba556-e49c-4104-ae0f-63e70c5476be',
    'kwargs': '{}',
    'name': 'testhtask',
    'time_start': 17871.679337502,
    'type': 'testhtask',
    'worker_pid': 23435},
    """
    i = _get_inspect()
    ret = []
    # task_info here is exactly same with i.query_task([id_])
    for task_info in i.active()[node_name]:
        ret.append({
            "id": task_info["id"],
            "name": task_info["name"],
            "start_time": task_info["time_start"]
        })

    return ret


def query_task(task_id):
    """Query task info by task_id.

    {'acknowledged': True,
     'args': '()',
     'delivery_info': {'exchange': '',
                       'priority': 0,
                       'redelivered': None,
                       'routing_key': 'celery'},
     'hostname': 'celery@ubuntu',
     'id': 'f2f090c4-832b-4fee-8152-76649383b940',
     'kwargs': '{}',
     'name': 'testhtask',
     'time_start': 17869.842484021,
     'type': 'testhtask',
     'worker_pid': 23434}]}
    """
    i = _get_inspect()
    return i.query_task([task_id])


def get_status():
    """Get Celery app status.

    {'broker': {'alternates': [],
                'connect_timeout': 4,
                'failover_strategy': 'round-robin',
                'heartbeat': 120.0,
                'hostname': 'localhost',
                'insist': False,
                'login_method': None,
                'port': 6379,
                'ssl': False,
                'transport': 'redis',
                'transport_options': {},
                'uri_prefix': None,
                'userid': None,
                'virtual_host': '9'},
     'clock': '553',
     'pid': 23426,
     'pool': {'max-concurrency': 4,
              'max-tasks-per-child': 'N/A',
              'processes': [23432, 23433, 23434, 23435],
              'put-guarded-by-semaphore': False,
              'timeouts': [0, 0],
              'writes': {'all': '33.33%, 33.33%, 33.33%',
                         'avg': '33.33%',
                         'inqueues': {'active': 0, 'total': 4},
                         'raw': '1, 1, 1',
                         'strategy': None,
                         'total': 3}},
     'prefetch_count': 16,
     'rusage': {'idrss': 0,
                'inblock': 0,
                'isrss': 0,
                'ixrss': 0,
                'majflt': 0,
                'maxrss': 43656,
                'minflt': 27202,
                'msgrcv': 0,
                'msgsnd': 0,
                'nivcsw': 98,
                'nsignals': 0,
                'nswap': 0,
                'nvcsw': 1315,
                'oublock': 0,
                'stime': 0.23726899999999998,
                'utime': 1.548287},
     'total': {'testhtask': 3}}       ->
    """
    i = _get_inspect()
    return i.stats()


def has_not_finished_task(task_id):
    """Check has some not finished task by task_id."""
    # 1. active task
    for task_info in get_active_task_list():
        if task_info["id"] == task_id:
            return True

    # 2. reserved task

    # 3. scheduled task

    return False


# -------------------------------------------------------------------------

# task operate


def celery_task_cancel(task_id):
    """Cancel specified celery task by task_id."""
    app_celery.control.revoke(task_id, terminate=True)


# -------------------------------------------------------------------------
