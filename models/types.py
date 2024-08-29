from enum import Enum
from typing import TypeAlias, Literal


class TaskType(Enum):
    MOBILE_AND_WEB_DEVELOPMENT: str = 'mobile and web development'
    SEO: str = 'seo'
    CONTENT_CREATION: str = 'content creation'
    ML_AND_AI: str = 'ml and ai'
    BLOCKCHAIN_SOLUTIONS: str = 'blockchain solutions'


task_type: TypeAlias = Literal[
    'mobile and web development',
    'seo',
    'content creation',
    'ml and ai',
    'blockchain solutions'
]


class TaskStatus(Enum):
    CREATED: str = 'created'
    SEEN: str = 'seen'
    ACCEPTED: str = 'accepted'
    REJECTED: str = 'rejected'


task_status: TypeAlias = Literal[
    'created',
    'seen',
    'accepted',
    'rejected'
]
