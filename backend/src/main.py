#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

from flask import Flask, request
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from flask_mongoengine import MongoEngine

from models import *
from tasks import *

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
        # 列表
        type_ = request.args.get("type", "all")
        author = request.args.get("author", "all")

        ret = []
        for sample in Sample.objects():
            ret.append(sample.json_ui())
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
        try:
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
                print(file.name)          # -> 'file'
                print(file.filename)      # -> '生成器.exe'
                # print(type(file.stream))  -> `tempfile.SpooledTemporaryFile`
                # print(file.stream.read()) -> 实际的数据
                # file.save('f.tmp')        -> 保存到本地磁盘
                # binary = file.stream.read()
                # sample = sample_check_exist_or_insert(binary)
                return "save success"
            else:
                return "invalid file"
        except Exception as e:
            print("异常: %s" % e)


# -------------------------------------------------------------------------

api.add_resource(TodoList, '/todos/')
api.add_resource(Todo, '/todos/<todo_id>/')
api.add_resource(TestIt, '/test/')

api.add_resource(SampleSimpleAction, '/sample/action/')
api.add_resource(SampleUpload, '/sample/upload/')

# -------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
