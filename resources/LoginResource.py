from http import HTTPStatus

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from models import UserModel


class LoginResource(Resource):
    path = '/login'

    @classmethod
    def post(cls) -> tuple[dict[str, str], HTTPStatus]:
        args = request.json
        print(args)
        login, password = args.get("login"), args.get("password")

        if not all([login, password]):
            return {"message": "Missing required fields"}, HTTPStatus.BAD_REQUEST

        try:
            user = UserModel.authenticate(login, password)

            if not user:
                return {"message": "incorrect login or password"}, HTTPStatus.UNAUTHORIZED
            else:
                access_token: str = create_access_token(identity=user.id)

            return {"access_token": access_token}, HTTPStatus.OK

        except ValueError as err:
            return {"message": str(err)}, HTTPStatus.BAD_REQUEST
