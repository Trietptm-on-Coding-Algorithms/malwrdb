#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

import hashlib

from models import *

from celery import Celery

node_name = "celery@ubuntu"  # we only have svr as 1 node.

app_celery = Celery('tasks', broker='redis://localhost:6379/9')
# app_celery.conf.result_backend = 'redis://localhost:6379/10'
stat = app_celery.events.State()

@app_celery.task(name="testhtask")
def hellox():
    import time
    while True:
        print('working...')
        time.sleep(3)


@app_celery.task(name="testhtask_success")
def hellox_success():
    print("i'm done!!!!")


@app_celery.task(name="testhtask_fail")
def hellox_fail():
    print("i'm dommmed!!!!")
    raise Exception("BOMMMMMM")


# -------------------------------------------------------------------------


def _get_inspect():
    return app_celery.control.inspect([node_name])  # celery@host_name


def celery_task_list_all():
    #
    i = _get_inspect()       
    task_name_list = i.registered()[node_name]
    ret = []
    for task_name in task_name_list:

        # ret.append(task_name)
        pass

    # global app_celery
    # print(app_celery.events.state)
    # print(stat)

    # print("events.state.tasks_by_timestamp():")

    """
    ['Task', 'Worker',  '_add_pending_task_child', '_clear', 
    '_clear_tasks', '_create_dispatcher', '_event', '_mutex', '_seen_types', '_taskheap', 
    '_tasks_by_type', '_tasks_by_worker', '_tasks_to_resolve', 'alive_workers', 'app', 'clear', 
    'clear_tasks', 'event', 'event_callback', 'event_count', 'freeze_while', 'get_or_create_task', 
    'get_or_create_worker', 'handlers', 'heap_multiplier', 'itertasks', 'max_tasks_in_memory', 
    'max_workers_in_memory', 'on_node_join', 'on_node_leave', 'rebuild_taskheap', 'task_count', 
    'task_event', 'task_types', 'tasks', 'tasks_by_time', 'tasks_by_timestamp', 'tasks_by_type', 
    'tasks_by_worker', 'worker_event', 'workers']

    """
    # print(len(stat.tasks))
    # for t in stat.tasks_by_time():
    #     pprint.pprint(t)
    # pprint.pprint(stat.tasks)

    # print("conf")
    # pprint.pprint(i.conf())
    """
    {'broker_url': 'redis://localhost:6379/9',
   'include': ['celery.app.builtins', 'tasks'],
   'result_backend': 'redis://localhost:6379/10'}
    """

    # print("active_queues")
    # pprint.pprint(i.active_queues())
    """
    [{'alias': None,
    'auto_delete': False,
    'binding_arguments': None,
    'bindings': [],
    'consumer_arguments': None,
    'durable': True,
    'exchange': {'arguments': None,
                 'auto_delete': False,
                 'delivery_mode': None,
                 'durable': True,
                 'name': 'celery',
                 'no_declare': False,
                 'passive': False,
                 'type': 'direct'},
    'exclusive': False,
    'expires': None,
    'max_length': None,
    'max_length_bytes': None,
    'max_priority': None,
    'message_ttl': None,
    'name': 'celery',
    'no_ack': False,
    'no_declare': None,
    'queue_arguments': None,
    'routing_key': 'celery'}]
    """

    # print("reserved")
    # pprint.pprint(i.reserved())   # received, and waiting to be executed
    """
    """

    # print("report")
    # pprint.pprint(i.report())  # no info about task
    """
    {'ok': '\n'
     'software -> celery:4.1.0 (latentcall) kombu:4.1.0 '
     'py:3.5.2\n'
     '            billiard:3.5.0.3 redis:2.10.6\n'
     'platform -> system:Linux arch:64bit, ELF '
     'imp:CPython\n'
     'loader   -> celery.loaders.app.AppLoader\n'
     'settings -> transport:redis '
     'results:redis://localhost:6379/10\n'
     '\n'
     "result_backend: 'redis://localhost:6379/10'\n"
     'include: \n'
     "    ('celery.app.builtins', 'tasks')\n"
     "broker_url: 'redis://localhost:6379/9'\n"}

    """
    
    # print("i.scheduled()")
    # pprint.pprint(i.scheduled())  # not active, waiting to be scheduled
    """
    """

    # print("stats:")
    # pprint.pprint(i.stats())
    """
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

    return ret


def celery_task_list_active():
    """
    active():
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
    task_list = i.active()[node_name]
    ret = []
    for task_info in task_list:
        # id_ = task_info["id"]
        # task_detail = i.query_task([id_])  # nothing more....
        """
         ['active',
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
        ret.append({
            "id": task_info["id"],
            "name": task_info["name"],
            "start_time": task_info["time_start"]
        })

    return ret


def celery_task_cancel(task_id):
    app_celery.control.revoke(task_id, terminate=True)


# -------------------------------------------------------------------------


def sample_check_exist_or_insert(sample_binary):
    """
    检查 sample 的 sha256, 没有则插入, 有则返回数据库中的 Sample
    """
    sha256 = hashlib.sha256(sample_binary.encode('utf-8')).hexdigest()

    q = Sample.objects(sha256=sha256)

    if q.count() == 0:
        # 没有, 插入
        sample = Sample()
        sample._binary = bytes(sample_binary, 'utf-8')
        sample.sha256 = sha256
        sample.save()
        return sample

    elif q.count() == 1:
        # 已存在, 且只有1个
        sample = q[0]
        return sample

    else:
        # 已存在, 且不止1个
        raise Exception("sample allready in database, and more than 1 items!!!")


# -------------------------------------------------------------------------
