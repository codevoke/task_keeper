from __future__ import annotations

from passlib.hash import pbkdf2_sha256

from .db import db, BaseModel
from .TaskModel import TaskModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    id: int        = db.Column(db.Integer, primary_key=True)
    email: str     = db.Column(db.String(120), unique=True, nullable=False)
    password: str  = db.Column(db.String(86), nullable=False)
    username: str  = db.Column(db.String(120), unique=True, nullable=False)
    verified: bool = db.Column(db.Boolean, default=False)

    def __init__(self, email: str, password: str, username: str):
        self.email = email
        self.password = password
        self.username = username

    def json(self) -> dict[str, int | str | bool]:
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'verified': self.verified
        }

    def get_tasks(self) -> list[TaskModel]:
        return TaskModel.query.filter_by(user_id=self.id).all()

    def __repr__(self) -> str:
        return '<User[%d] %r>' % (self.id, self.username)

    @classmethod
    def get_by_id(cls, _id: int) -> UserModel:
        return cls.query.get(_id)

    @classmethod
    def authenticate(cls, email: str, password: str) -> UserModel | None:
        user = cls.get_by_email(email)
        if not user:
            return
        if not pbkdf2_sha256.verify(password, user.password):
            raise ValueError('Invalid password')
        return user

    @classmethod
    def get_by_email(cls, email: str) -> UserModel:
        return cls.query.filter_by(email=email).first()

