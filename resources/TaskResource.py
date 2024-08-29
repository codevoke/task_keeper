from http import HTTPStatus

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import TaskModel


class TaskResource(Resource):
    path: str = '/task/<id>'

    @classmethod
    def get(cls, id: str) -> tuple[dict[str, str], HTTPStatus]:
        try:
            id: int = int(id)
        except ValueError:
            return {"message": "id must be an integer"}, HTTPStatus.BAD_REQUEST

        task = TaskModel.find_by_id(id)
        if task is None:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND
        else:
            return task.json(), HTTPStatus.OK

    @classmethod
    @jwt_required()
    def post(cls, id: str) -> tuple[dict[str, str], HTTPStatus]:
        if id != "new":
            return {"message": "fuck you, change http request method"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        args: dict[str, str | int] = request.json
        print(args)
        # parse args
        title: str       = args.get('title')
        description: str = args.get('description')
        contacts: str    = args.get('contacts')
        type: str        = args.get('type')

        if not all([title, description, type]):
            return {"message": "title, description and type are required"}, HTTPStatus.BAD_REQUEST

        user_id: int = int(get_jwt_identity())

        # create task
        task = TaskModel(
            title=title,
            description=description,
            contacts=contacts,
            _type=type,
            author_id=user_id,
        )
        task.save()
        return task.json(), HTTPStatus.CREATED

