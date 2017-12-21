#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

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
    "port": 27017,
    "username": "lyclovechl",
    "password": "yGeIgWof97zXrzayOwcIhIaF5EqcUR",
    "authentication_source": "admin",
    "db": "malwrdb"
}
db = MongoEngine(app)


# -------------------------------------------------------------------------

# Restful
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

## 测试
class TestIt(Resource):
    def get(self):
        print("test it")
        print(request.args)
        return TODOS

# -------------------------------------------------------------------------


class Action(Resource):
    def get(self):
        print("-" * 100)
        ret = self._get()
        print(ret)
        print("+" * 100)
        return ret

    def _get(self):
        try:
            action = request.args.get("action", None)
            if not action:
                return "no action provided!"

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
                return "invalid action: %s" % action

        except Exception as e:
            import traceback
            traceback.print_exc()
            return "exception!"

    def get_refGroupList(self):
        # get all groups
        ret = []
        for group in RefGroup.objects():
            ret.append(group.json_ui())
        return ret

    def get_topRefDirs(self):
        # get top RefDir by group_id
        group_id = request.args.get("group_id", None)
        if not group_id:
            return "no group_id provided!"

        q_group = RefGroup.objects(group_id=group_id)
        if q_group.count() != 1:
            return "no or too many group by group_id"
        group = q_group[0]

        q_dir = RefDir.objects(refGroup=group, parnetRefDir=None)
        if q_dir.count() != 1:
            return "no or too many top RefDir by group_id"

        # return a list, instead of standalone obj, to make it easier for frontend
        return [q_dir[0].json_ui()]

    def get_subRefDirs(self):
        # get sub RefDir list by parent RefDir id
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            return "no refDir id provided!"

        q_refDir = RefDir.objects(pk=ref_dir_id)
        if q_refDir.count() != 1:
            return "no or too many refDir by ref_dir_id"
        ref_dir_cur = q_refDir[0]

        ret =[]
        for ref_dir in RefDir.objects(parnetRefDir=ref_dir_cur):
            ret.append(ref_dir.json_ui())
        return ret

    def get_subSamples(self):
        # get sub Sample list by parent refDir id
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            return "no refDir id provided!"

        q_refDir = RefDir.objects(pk=ref_dir_id)
        if q_refDir.count() != 1:
            return "no or too many refDir by ref_dir_id"
        ref_dir_cur = q_refDir[0]

        ret = []
        for sample_belongto in SampleBelongTo.objects(refDir=ref_dir_cur):
            q_sample = Sample.objects(pk=sample_belongto.sample_id)
            if q_sample.count() != 1:
                return "no or too many sample by sample_id"
            ret.append(q_sample[0].json_ui())
        return ret

    def get_subRefFiles(self):
        # get sub RefFile list by parent refDir id
        ref_dir_id = request.args.get("refDir_id", None)
        if not ref_dir_id:
            return "no refDir id provided!"

        q_refDir = RefDir.objects(pk=ref_dir_id)
        if q_refDir.count() != 1:
            return "no or too many refDir by ref_dir_id"
        ref_dir_cur = q_refDir[0]

        ret = []
        for file_belongto in RefFileBelongTo.objects(refDir=ref_dir_cur):
            q_refFile = RefFile.objects(pk=file_belongto.ref_file_id)
            if q_refFile.count() != 1:
                return "no or too many refFile by ref_file_id"
            ret.append(q_refFile[0].json_ui())
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
        print("-" * 100)
        ret = self._post()
        print(ret)
        print("+" * 100)
        return ret

    def _post(self):
        try:
            file = request.files['file']
            if not file:
                return "no file uploaded!"

            type_ =  request.args.get("type", None)
            if not type_:
                return "no upload type provided!"

            if type_ == "sample_group":
                return self.upload_by_group(file)

            elif type_ == "sample_standalone":
                return self.upload_standalone_sample(file)

            elif type_ == "sample_parent":
                return self.upload_by_parent(file)

            else:
                return "invalid upload type: %s" % type_
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
            import traceback
            traceback.print_exc()
            return "exception!"

    def upload_by_group(self, file_):
        group_id = request.args.get("group_id", None)
        relative_path = request.args.get("relative_path", None)
        if not group_id or not relative_path:
            return "invalid args!"

        # check if group_id already exists
        q_refGroup = RefGroup.objects(group_id=group_id)
        if q_refGroup.count() > 1:
            return "group with same group_id more than 1, error!"

        # get refGroup and refDir
        if q_refGroup.count() == 0:
            # no group, create one group and relative dir
            tar_refGroup = RefGroup()
            tar_refGroup.group_id = group_id
            tar_refGroup.save()
            print("create tar_refGroup with group_id: %s" % group_id)
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
                print(dir_tmp.refGroup)
                print("(1st)create dir with name: %s" % dir_str)
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
                        return "get top dir of file fail!"
                    dir_tmp = q[0]
                    tar_refDir = dir_tmp
                else:
                    q = RefDir.objects(refGroup=tar_refGroup, parnetRefDir=dir_tmp, dir_name=dir_str)
                    if q.count() > 1:
                        return "get dir of file fail!"
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
                        print("create dir with name: %s" % dir_str)

        assert tar_refGroup and tar_refDir

        # check if file with same sha256 exists

        _binary = file_.stream.read()

        if len(_binary) == 0:
            # empty file
            # may store as EMPTY ref file if not already exists
            q_refFile = RefFile.objects(file_size=0)
            if q_refFile.count() > 1:
                return "ref file with 0 size exists more than 1, error!: %s" % (relative_path)
            if q_refFile.count() == 1:
                ref_file = q_refFile[0]
            else:
                ref_file = RefFile()
                ref_file.save()
            # add link
            link = RefFileBelongTo()
            link.refGroup = tar_refGroup
            link.refDir = tar_refDir
            link.ref_file_id = ref_file.pk
            link.file_name = file_.filename
            link.file_relative_path = relative_path
            return "save empty file as refFile"

        import hashlib
        sha256 = hashlib.sha256(_binary).hexdigest()
        q_sample = Sample.objects(sha256=sha256)
        if q_sample.count() > 1:
            return "sample with same sha256 exists and more than 1: %s - %d" % (sha256, q.count())

        if q_sample.count() == 1:
            if RefFile.objects(sha256=sha256).count() != 0:
                return "file exists both as sample and ref file. error!: %s" % sha256

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
            return "sample already exists, save sample_belongto"

        else:
            q_refFile = RefFile.objects(sha256=sha256)
            if q_refFile.count() > 1:
                return "ref file with same sha256 exists and more than 1: %s - %d" % (sha256, q.count())

            if q_refFile.count() == 1:

                # file exists as ref file -> update database
                ref_file = q_refFile[0]
                print("refFile already exists")

            else:
                # file not exists in database -> store in database (as ref file) and update something
                ref_file = RefFile()
                ref_file._binary = _binary
                ref_file.save()
                print("save file as ref file")

            ref_file_belongto = RefFileBelongTo()
            ref_file_belongto.refGroup = tar_refGroup
            print(tar_refDir)
            ref_file_belongto.refDir = tar_refDir
            ref_file_belongto.ref_file_id = str(ref_file.pk)
            ref_file_belongto.file_name = file_.filename
            ref_file_belongto.file_relative_path = relative_path
            ref_file_belongto.save()
            print("save ref_file_belongto")

            return "save file as ref file"

    def upload_standalone_sample(self, file_):
        pass

    def upload_by_parent(self, file_):
        pass

# -------------------------------------------------------------------------

api.add_resource(TodoList, '/todos/')
api.add_resource(Todo, '/todos/<todo_id>/')
api.add_resource(TestIt, '/test/')

api.add_resource(Action, '/action/')

api.add_resource(SampleSimpleAction, '/sample/action/')
api.add_resource(SampleUpload, '/sample/upload/')

# -------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
