from uuid import UUID, uuid4

from flask.wrappers import Request as FlaskRequest
from pydantic import BaseModel, Field


class RequestModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    message: str

    @classmethod
    def create_from_flask(cls, flask_request: FlaskRequest) -> "RequestModel":
        body = flask_request.get_json()
        return cls(**body)
