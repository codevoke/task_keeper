from __future__ import annotations

from sqlalchemy.orm import relationship

from .db import db, BaseModel
from .types import TaskType, task_type, TaskStatus, task_status


class TaskModel(BaseModel):
    __tablename__ = 'tasks'

    id: int            = db.Column(db.Integer, primary_key=True)
    title: str         = db.Column(db.String(50))
    type: TaskType     = db.Column(db.Enum(TaskType))
    status: TaskStatus = db.Column(db.Enum(TaskStatus), default=TaskStatus.CREATED)
    description: str   = db.Column(db.String)
    contacts: str      = db.Column(db.String, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title: str, _type: task_type, description: str, contacts: str, author_id: int):
        self.title = title
        self.description = description
        self.contacts = contacts
        self.author_id = author_id
        try:
            _type: str = _type.lower()  # "SEO" -> "seo" for usability
            self.type = TaskType(_type)
        except ValueError:
            raise ValueError('Invalid task type')

    def json(self) -> dict[str, int | str]:
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type.value,
            'status': self.status.value,
            'description': self.description,
            'contacts': self.contacts
        }

    def set_status(self, status: task_status) -> None:
        try:
            self.status = TaskStatus(status)
            self.save()
        except ValueError:
            raise ValueError('Invalid task status')
        
    @classmethod
    def get_all_tasks(cls) -> list[TaskModel] | None:
        tasks = cls.query.all()
        if tasks:
            for task in tasks:
                if task.status == TaskStatus.CREATED:
                    task.set_status(TaskStatus.SEEN.value)
            return tasks
        else:
            return None

    @classmethod
    def get_by_author(cls, author_id: int) -> list[TaskModel]:
        return cls.query.filter_by(author_id=author_id).all()

    @classmethod
    def get_by_id(cls, _id: int) -> TaskModel:
        return cls.query.get(_id)
