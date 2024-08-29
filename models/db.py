from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db: SQLAlchemy = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.app_context().push()
    db.create_all()


class BaseModel(db.Model):
    __abstract__ = True
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
