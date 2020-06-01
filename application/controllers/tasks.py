from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from application.models.task import Task
from application import db

task_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'user_id': fields.Integer
}

task_list_fields = {
    'count': fields.Integer,
    'tasks': fields.List(fields.Nested(task_fields)),
}

task_post_parser = reqparse.RequestParser()
task_post_parser.add_argument(
    'name',
    type=str,
    required=True,
    location=['json'],
    help='name parameter is required'
)
task_post_parser.add_argument(
    'description',
    type=str,
    required=True,
    location=['json'],
    help='description parameter is required'
)
task_post_parser.add_argument(
    'user_id',
    type=int,
    required=True,
    location=['json'],
    help='user_id parameter is required'
)


class TasksResource(Resource):
    def get(self, task_id=None):
        if task_id:
            task = Task.query.filter_by(id=task_id).first()
            return marshal(task, task_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            task = Task.query.filter_by(**args).order_by(Task.id)
            if limit:
                task = task.limit(limit)

            if offset:
                task = task.offset(offset)

            task = task.all()

            return marshal({
                'count': len(task),
                'tasks': [marshal(t, task_fields) for t in task]
            }, task_list_fields)

    @marshal_with(task_fields)
    def post(self):
        args = task_post_parser.parse_args()

        task = Task(**args)
        db.session.add(task)
        db.session.commit()

        return task

    @marshal_with(task_fields)
    def put(self, task_id=None):
        task = Task.query.get(task_id)

        if 'name' in request.json:
            task.name = request.json['name']

        if 'description' in request.json:
            task.description = request.json['description']

        db.session.commit()
        return task

    @marshal_with(task_fields)
    def delete(self, task_id=None):
        task = Task.query.get(task_id)

        db.session.delete(task)
        db.session.commit()

        return task