from http import HTTPStatus
import json

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from models import UserModel


class AdminLoginResource(Resource):
    path = '/login'

    @classmethod
    def post(cls) -> tuple[dict[str, str], HTTPStatus]:
        args = request.json
        password: str = args.get("password")

        if not password:
            return {"message": "Missing password field"}, HTTPStatus.BAD_REQUEST

        true_password = json.loads(open('admin_resources/data.json', 'r').read()).get("admin-password")

        if password != true_password:
            return {"message": "incorrect password"}, HTTPStatus.UNAUTHORIZED
        else:
            access_token: str = create_access_token(identity="admin")

        return {"access_token": access_token}, HTTPStatus.OK
