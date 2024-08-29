from __future__ import annotations

from .db import db, BaseModel
from .UserModel import UserModel


class VerifyCodeModel(BaseModel):
    __tablename__ = 'verify_code'

    id: int      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code: str    = db.Column(db.String(6), nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, code: str, user_id: int):
        self.code = code
        self.user_id = user_id

    def verify_code(self, code: str):
        if self.code != code:
            raise ValueError("invalid code")
        else:
            user = UserModel.get_by_id(self.user_id)
            if not user:
                raise ValueError("user not found")
            user.verified = True
            user.save()
            self.delete()

    @classmethod
    def get_by_user_id(cls, user_id: int) -> VerifyCodeModel:
        return cls.query.filter_by(user_id=user_id).first()

    def __repr__(self):
        return '<VerifyCodeModel %r>' % self.id
