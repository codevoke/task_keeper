from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from .LoginResource import AdminLoginResource
from .TaskResource import AdminTaskResource


resources = [
    AdminLoginResource,
    AdminTaskResource
]

api: Api | None = None
jwt: JWTManager | None = None


def init_app(app: Flask):
    global api, jwt
    api = Api(app, prefix='/api/admin')
    jwt = JWTManager(app)
    register_resources()


def register_resources():
    global resources
    for resource in resources:
        api.add_resource(resource, resource.path)
