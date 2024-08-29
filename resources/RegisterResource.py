from http import HTTPStatus

from flask_restful import Resource
from flask import request

from models import UserModel, VerifyCodeModel
from utils import hash_password, send_email_async, validate_email, make_code


class RegisterResource(Resource):
    path: str = '/register'

    @classmethod
    def post(cls) -> tuple[dict[str, str], HTTPStatus]:
        args: dict[str, str | int] = request.json
        # parse args
        name: str | None = args.get('name')
        email: str | None = args.get('email')
        password: str | None = args.get('password')

        if not all([name, password, email]):
            return {'message': 'Missing arguments'}, HTTPStatus.BAD_REQUEST

        if not validate_email(email):
            return {'message': 'Invalid email'}, HTTPStatus.BAD_REQUEST

        code: str = make_code()
        print(args)
        user: UserModel = UserModel(
            username=name,
            password=hash_password(password),
            email=email
        )
        user.save()
        print(user.json)
        verify_code: VerifyCodeModel = VerifyCodeModel(
            code=code,
            user_id=user.id
        )
        verify_code.save()
        # send email
        send_email_async(email, name, code)
        return {
            'message': 'User created successfully. Now you need verify your email'
        }, HTTPStatus.CREATED
