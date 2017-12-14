#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from flask_mongoengine import mongoengine

# -------------------------------------------------------------------------

class LogLine(mongoengine.Document):
    """日志"""
    meta = {'collection': "log_line"}

    file = mongoengine.StringField()                     # 代码文件
    level = mongoengine.IntField()                       # 级别
    info = mongoengine.StringField()                     # 信息
    time = mongoengine.DateTimeField()                   # 时间

    def clean(self):
        self.time = datetime.now()


class Sample(mongoengine.Document):
    """样本"""
    meta = {'collection': "sample"}

    _binary = mongoengine.BinaryField()                                            # 二进制数据

    file_name = mongoengine.StringField()                                          # 文件名, 添加时设置. 不是路径
    sample_size = mongoengine.IntField()                                           # 样本大小
    file_type = mongoengine.StringField()                                          # 样本文件类型

    md5 = mongoengine.StringField(max_length=32, min_length=32)                    # 哈希值 - MD5    - 长度32
    sha1 = mongoengine.StringField(max_length=40, min_length=40)                   # 哈希值 - SHA1   - 长度40
    sha256 = mongoengine.StringField(max_length=64, min_length=64)                 # 哈希值 - SHA256 - 长度64
    sha512 = mongoengine.StringField(max_length=128, min_length=128)               # 哈希值 - SHA512 - 长度128
    ssdeep = mongoengine.StringField()                                             # 哈希值 - ssdeep
    imphash = mongoengine.StringField()                                            # 哈希值 - 导入表
    crc32 = mongoengine.StringField()                                              # 哈希值 - CRC32

    platform = mongoengine.StringField()                                           # 平台
    is_malicious = mongoengine.BooleanField()                                      # 是否恶意
    malware_name_list = mongoengine.ListField()                                    # 恶意名称列表(某些恶意代码有多个名称)
    malware_family_list = mongoengine.ListField()                                  # 恶徒家族列表

    parent__sample_id = mongoengine.ObjectIdField()                                # 父样本 id
    parent__sample_to_this_type = mongoengine.StringField()                        # 与父样本的关系(有choices)

    #

    analyze_time = mongoengine.DateTimeField()                                     # 分析时间(手动设置). 为 None 表示没分析过

    update_time = mongoengine.DateTimeField()

    def clean(self):
        pass

    def to_filter(self):
        return {"sha256": self.sha256}

    def json_ui(self):
        """返回到界面的 Json"""
        ret = json.loads(self.to_json())
        print(type(ret))

        del ret["_binary"]
        return ret

# -------------------------------------------------------------------------
