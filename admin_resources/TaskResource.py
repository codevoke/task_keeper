from http import HTTPStatus

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import TaskModel


class AdminTaskResource(Resource):
    path: str = '/tasks'

    @classmethod
    def get(cls) -> tuple[dict[str, str], HTTPStatus]:
        tasks: list[TaskModel] = TaskModel.get_all_tasks()
        
        if tasks is None or len(tasks) == 0:
            return {"message": "tasks not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"tasks": [task.json() for task in tasks]}, HTTPStatus.OK

    @classmethod
    @jwt_required()
    def put(cls) -> tuple[dict[str, str], HTTPStatus]:
        args = request.json
        
        id: str = args.get('id')
        status: str = args.get('status')

        try:
            task: TaskModel = TaskModel.get_by_id(id)
            if not task:
                return {"message": "task not found"}, HTTPStatus.NOT_FOUND
            task.set_status(status)
            return {"message": "task updated"}, HTTPStatus.OK
        except ValueError as e:
            return {"message": str(e)}, HTTPStatus.NOT_FOUND