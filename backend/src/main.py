#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

import traceback

from flask import Flask, request
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from flask_mongoengine import MongoEngine

from models import *
from tasks import *
from utils import *

# -------------------------------------------------------------------------

app = Flask(__name__)

# 跨站
CORS(app, supports_credentials=True)

# MongoDB 数据库
app.config["MONGODB_SETTINGS"] = {
    "host": "127.0.0.1",
    "port": 27019,
    "username": "lyclovechl",
    "password": "yGeIgWof97zXrzayOwcIhIaF5EqcUR",
    "authentication_source": "admin",
    "db": "malwrdb"
}
db = MongoEngine(app)


# -------------------------------------------------------------------------

from log import log


def warn(info):
    log(__file__, info, "warn")


def error(info):
    log(__file__, info, "error")


def debug(info):
    log(__file__, info, "debug")


# -------------------------------------------------------------------------

# Restful
api = Api(app)

# -------------------------------------------------------------------------


class LogLineAction(Resource):
    def get(self):
        print("-" * 30 + "LogLine Action Start" + "-" * 30)
        ret = self._get()
        print(ret)
        print("+" * 30 + "LogLine Action End" + "+" * 30)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                raise Exception("no action provided!")

            print("action: " + action)

            if action == "get_logLines":
                return self.get_logLines()

            elif action == "clearLogLines":
                return self.clearLogLines()

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception!"

    def get_logLines(self):
        # get log Lines
        ret = []
        for log in LogLine.objects.order_by("-add_time"):
            ret.append(log.json_ui())
        return ret

    def clearLogLines(self):
        # clear logLines
        LogLine.drop_collection()
        return "success"


class Action(Resource):
    # some actions for group/sample/file
    def get(self):
        print("-" * 30 + "Action Start" + "-" * 30)
        ret = self._get()
        print(ret)
        print("+" * 30 + "Action End" + "+" * 30)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                raise Exception("no action provided!")

            if action == "get_refGroupList":
                return self.get_refGroupList()

            elif action == "get_topRefDirs":
                return self.get_topRefDirs()

            elif action == "get_subRefDirs":
                return self.get_subRefDirs()

            elif action == "get_subSamples":
                return self.get_subSamples()

            elif action == "get_subRefFiles":
                return self.get_subRefFiles()

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception!"

    def get_refGroupList(self):
        # get all groups
        pageSize = request.args.get("pageSize", None)
        pageIndex = request.args.get("pageIndex", None)
        if not pageSize or not pageIndex:
            raise Exception("no pageSize or pageIndex provided!")
        pageSize = int(pageSize)
        pageIndex = int(pageIndex)

        ret = {"group_length": RefGroup.objects.count()}

        group_list = []
        for group in RefGroup.objects.order_by("-update_time").skip(pageIndex*pageSize).limit(pageSize):
            group_list.append(group.json_ui())
        ret["group_list"] = group_list

        return ret

    def get_topRefDirs(self):
        # get top RefDir by group_id
        group_id = request.args.get("group_id", None)
        if not group_id:
            raise Exception("no group_id provided!")

        q_group = RefGroup.objects(group_id=group_id)
        if q_group.count() != 1:
            raise Exception("no or too many group by group_id")
        group = q_group[0]

        q_dir = RefDir.objects(refGroup=group, parnetRefDir=None)
        if q_dir.count() != 1:
            raise Exception("no or too many top RefDir by group_id")

        # return a list, instead of standalone obj, to make it easier for frontend
        return [q_dir[0].json_ui()]

    def get_subRefDirs(self):
        # get sub RefDir list by parent RefDir id
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            raise Exception("no refDir id provided!")

        q_refDir = RefDir.objects(pk=ref_dir_id)
        if q_refDir.count() != 1:
            raise Exception("no or too many refDir by ref_dir_id")
        ref_dir_cur = q_refDir[0]

        ret =[]
        for ref_dir in RefDir.objects(parnetRefDir=ref_dir_cur):
            ret.append(ref_dir.json_ui())
        return ret

    def get_subSamples(self):
        # get sub Sample list by parent refDir id
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            raise Exception("no refDir id provided!")

        q_refDir = RefDir.objects(pk=ref_dir_id)
        if q_refDir.count() != 1:
            raise Exception("no or too many refDir by ref_dir_id")
        ref_dir_cur = q_refDir[0]

        ret = []
        for sample_belongto in SampleBelongTo.objects(refDir=ref_dir_cur):
            q_sample = Sample.objects(pk=sample_belongto.sample_id)
            if q_sample.count() != 1:
                raise Exception("no or too many sample by sample_id")
            sample = q_sample[0].json_ui()
            sample["sample_name"] = sample_belongto.sample_name
            ret.append(sample)
        return ret

    def get_subRefFiles(self):
        # get sub RefFile list by parent refDir id
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            raise Exception("no refDir id provided!")

        q_refDir = RefDir.objects(pk=ref_dir_id)
        if q_refDir.count() != 1:
            raise Exception("no or too many refDir by ref_dir_id")
        ref_dir_cur = q_refDir[0]

        ret = []
        for file_belongto in RefFileBelongTo.objects(refDir=ref_dir_cur):
            q_refFile = RefFile.objects(pk=file_belongto.ref_file_id)
            if q_refFile.count() != 1:
                raise Exception("no or too many refFile by ref_file_id")
            ref_file = q_refFile[0].json_ui()
            ref_file["file_name"] = file_belongto.file_name
            ret.append(ref_file)
        return ret


class SampleSimpleAction(Resource):
    """针对样本的各种简单行为"""
    def get(self):
        try:
            return self._get()
        except Exception as e:
            print("异常: SampleSimpleAction: %s" % e)

    def _get(self):
        action = request.args.get("action", None)
        if not action:
            return "无效的行为类型"

        if action == "count":
            return self._count()

        elif action == "check_exists":
            return self._check_exists()

        elif action == "list":
            return self._list()

        else:
            return "不支持的操作类型"

    def _count(self):
        # 计数
        type_ = request.args.get("type", "all")
        author = request.args.get("author", "all")

        print("get sample count: type: %s, author: %s" % (type_, author))

        return Sample.objects.count()

    def _list(self):
        # list of refGroup, sorted by update_time
        type_ = request.args.get("type", "all")
        author = request.args.get("author", "all")

        ret = []
        for group in RefGroup.objects():
            ret.append(group.json_ui())
        return ret

    def _check_exists(self):
        # 检查是否存在
        sha256 = request.args.get("sha256", None)
        if not sha256:
            return "无效的 SHA256"

        return Sample.objects(sha256=sha256).count() != 0


class SampleUpload(Resource):
    """样本上传"""
    def post(self):
        print("-" * 30 + "Sample Upload Start" + "-" * 30)
        ret = self._post()
        print(ret)
        print("+" * 30 + "Sample Upload End" + "+" * 30)
        return ret

    def _post(self):
        try:
            file = request.files['file']
            if not file:
                raise Exception("no file uploaded!")

            type_ =  request.args.get("type", None)
            if not type_:
                raise Exception("no upload type provided!")

            if type_ == "sample_group":
                return self.upload_by_group(file)

            elif type_ == "sample_standalone":
                return self.upload_standalone_sample(file)

            elif type_ == "sample_parent":
                return self.upload_by_parent(file)

            else:
                raise Exception("invalid upload type: %s" % type_)
            """
            import pprint
            # pprint.pprint(dir(request))
            # print(request.headers)
            print(request.files)
            print(request.form)
            print(request.args)
            file = request.files['file']
            if file:
                # pprint.pprint(dir(file))
                # print(type(file))         -> werkzeug.datastructures.FileStorage
                # print(file.name)          # -> 'file'
                # print(file.filename)      # -> '生成器.exe'
                # print(type(file.stream))  -> `tempfile.SpooledTemporaryFile`
                # print(file.stream.read()) -> 实际的数据
                # file.save('f.tmp')        -> 保存到本地磁盘
                # binary = file.stream.read()
                # sample = sample_check_exist_or_insert(binary)
                return "save success"
            else:
                return "invalid file"
            """
        except Exception as e:
            error(traceback.format_exc())
            return "exception!"

    def upload_by_group(self, file_):
        group_id = request.args.get("group_id", None)
        relative_path = request.args.get("relative_path", None)
        if not group_id or not relative_path:
            raise Exception("invalid args!")

        # check if group_id already exists
        q_refGroup = RefGroup.objects(group_id=group_id)
        if q_refGroup.count() > 1:
            raise Exception("group with same group_id more than 1, error!")

        # get refGroup and refDir
        if q_refGroup.count() == 0:
            # no group, create one group and relative dir
            tar_refGroup = RefGroup()
            tar_refGroup.group_id = group_id
            tar_refGroup.save()
            debug("create tar_refGroup with group_id: %s" % group_id)
            dir_str_list = path_to_dirs(relative_path)
            tar_refDir = None
            for index, dir_str in enumerate(dir_str_list):
                dir_tmp = RefDir()
                dir_tmp.dir_name = dir_str
                dir_tmp.refGroup = tar_refGroup
                if index != 0:
                    assert tar_refDir
                    dir_tmp.parnetRefDir = tar_refDir
                dir_tmp.save()
                tar_refDir = dir_tmp
                debug("(1st)create dir with name: %s" % dir_str)
        else:
            # already has group, get target dir
            tar_refGroup = q_refGroup[0]
            dir_tmp = None
            dir_str_list = path_to_dirs(relative_path)
            tar_refDir = None
            for index, dir_str in enumerate(dir_str_list):
                if index == 0:
                    q = RefDir.objects(refGroup=tar_refGroup, parnetRefDir=None)
                    if q.count() != 1:
                        raise Exception("get top dir of file fail!")
                    dir_tmp = q[0]
                    tar_refDir = dir_tmp
                else:
                    q = RefDir.objects(refGroup=tar_refGroup, parnetRefDir=dir_tmp, dir_name=dir_str)
                    if q.count() > 1:
                        raise Exception("get dir of file fail!")
                    if q.count() == 1:
                        dir_tmp = q[0]
                        tar_refDir = dir_tmp
                        continue
                    else:
                        # now we need to create dir
                        dir_tmp = RefDir()
                        dir_tmp.dir_name = dir_str
                        dir_tmp.refGroup = tar_refGroup
                        dir_tmp.parnetRefDir = tar_refDir
                        dir_tmp.save()
                        tar_refDir = dir_tmp
                        debug("create dir with name: %s" % dir_str)

        assert tar_refGroup and tar_refDir

        # check if file with same sha256 exists

        _binary = file_.stream.read()

        if len(_binary) == 0:
            # empty file
            # may store as EMPTY ref file if not already exists
            q_refFile = RefFile.objects(file_size=0)
            if q_refFile.count() > 1:
                raise Exception("ref file with 0 size exists more than 1, error!: %s" % (relative_path))
            if q_refFile.count() == 1:
                ref_file = q_refFile[0]
            else:
                ref_file = RefFile()
                ref_file.save()
            # add link
            link = RefFileBelongTo()
            link.refGroup = tar_refGroup
            link.refDir = tar_refDir
            link.ref_file_id = str(ref_file.pk)
            link.file_name = file_.filename
            link.file_relative_path = relative_path
            link.save()
            debug("save empty file as refFile")
            return "upload success"

        import hashlib
        sha256 = hashlib.sha256(_binary).hexdigest()
        q_sample = Sample.objects(sha256=sha256)
        if q_sample.count() > 1:
            raise Exception("sample with same sha256 exists and more than 1: %s - %d" % (sha256, q.count()))

        if q_sample.count() == 1:
            if RefFile.objects(sha256=sha256).count() != 0:
                raise Exception("file exists both as sample and ref file. error!: %s" % sha256)

            # file only exists as sample -> update database
            sample = q_sample[0]
            sample_belongto = SampleBelongTo()
            sample_belongto.refGroup = tar_refGroup
            sample_belongto.refDir = tar_refDir
            sample_belongto.sample_id = str(sample.pk)
            sample_belongto.sample_name = file_.filename
            sample_belongto.sample_relative_path = relative_path
            sample_belongto.save()
            print("sample already exists, save sample_belongto")
            return "upload success"

        else:
            q_refFile = RefFile.objects(sha256=sha256)
            if q_refFile.count() > 1:
                raise Exception("ref file with same sha256 exists and more than 1: %s - %d" % (sha256, q.count()))

            if q_refFile.count() == 1:

                # file exists as ref file -> update database
                ref_file = q_refFile[0]
                debug("refFile already exists")

            else:
                # file not exists in database -> store in database (as ref file) and update something
                ref_file = RefFile()
                ref_file._binary = _binary
                ref_file.save()
                debug("save file as ref file")

            ref_file_belongto = RefFileBelongTo()
            ref_file_belongto.refGroup = tar_refGroup
            ref_file_belongto.refDir = tar_refDir
            ref_file_belongto.ref_file_id = str(ref_file.pk)
            ref_file_belongto.file_name = file_.filename
            ref_file_belongto.file_relative_path = relative_path
            ref_file_belongto.save()
            debug("save ref_file_belongto")

            return "upload success"

    def upload_standalone_sample(self, file_):
        pass

    def upload_by_parent(self, file_):
        pass


class RefFileActioin(Resource):
    def post(self):
        print("-" * 30 + "RefFile Action Start" + "-" * 30)
        ret = self._post()
        print(ret)
        print("+" * 30 + "RefFile Action End" + "+" * 30)
        return ret

    def _post(self):
        try:
            args = json.loads(request.data)
            if "action" not in args:
                raise Exception("no action!")

            action = args["action"]
            if action == "analyzeAsSample":
                return self.analyzeAsSample(args)

            else:
                raise Exception("invalid action: %s" % action)

        except Exception as e:
            error(traceback.format_exc())
            return "exception:\n" + str(e)

    def analyzeAsSample(self, args):
        #
        if "refFileId" not in args:
            raise Exception("no ref file id provided!")

        ref_file_id = args["refFileId"]
        return "Analyzing...."


# -------------------------------------------------------------------------

api.add_resource(LogLineAction, '/logline/')
api.add_resource(Action, '/action/')

api.add_resource(RefFileActioin, '/reffile/')

api.add_resource(SampleSimpleAction, '/sample/action/')
api.add_resource(SampleUpload, '/sample/upload/')

# -------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
