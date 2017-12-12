from flask import Flask, request
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)

# 跨站
CORS(app, supports_credentials=True)

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

## Test
class TestIt(Resource):
    def get(self):
        print("test it")
        print(request.args)
        return TODOS

## 样本上传
class SampleUpload(Resource):
    def post(self):
        file = request.files['file']
        if file:
            # print(type(file))         -> werkzeug.datastructures.FileStorage
            # print(file.name)          -> 'file'
            # print(file.filename)      -> '生成器.exe'
            # print(type(file.stream))  -> `tempfile.SpooledTemporaryFile`
            # print(file.stream.read()) -> 实际的数据
            # file.save('f.tmp')        -> 保存到本地磁盘
            return "save success"
        else:
            return "invalid file"
##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos/')
api.add_resource(Todo, '/todos/<todo_id>/')
api.add_resource(TestIt, '/test/')
api.add_resource(SampleUpload, '/sample_upload/')


if __name__ == '__main__':
    app.run(debug=True)
