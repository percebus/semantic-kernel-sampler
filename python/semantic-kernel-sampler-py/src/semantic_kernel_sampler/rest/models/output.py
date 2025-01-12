from typing import Any

from flask import jsonify
from flask.wrappers import Response as FlaskResponse
from pydantic import BaseModel


class OutputModel(BaseModel):
    def to_flask(self) -> FlaskResponse:
        _response: dict[str, Any] = self.model_dump()
        return jsonify(_response)
