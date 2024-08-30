from http import HTTPStatus

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import VerifyCodeModel


class VerifyAccountResource(Resource):
    path = '/confirm-email'

    @classmethod
    @jwt_required()
    def post(cls) -> tuple[dict[str, str], HTTPStatus]:
        args: dict[str, str]= request.json
        print(args)
        code: str = args.get('code')

        if not code:
            return {"message": "Missing required fields"}, HTTPStatus.BAD_REQUEST

        try:
            user_id: int = int(get_jwt_identity())
            print(f"{user_id=}")
            vcm: VerifyCodeModel = VerifyCodeModel.get_by_user_id(user_id)
            if not vcm:
                return {"message": "user not found"}, 400
            vcm.verify_code(code)
            return {"message": "successfully verify account"}, HTTPStatus.OK

        except ValueError as err:
            return {"message": str(err)}, HTTPStatus.BAD_REQUEST
