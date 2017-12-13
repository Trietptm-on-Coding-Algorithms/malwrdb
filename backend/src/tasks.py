#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

import hashlib

from models import *

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
