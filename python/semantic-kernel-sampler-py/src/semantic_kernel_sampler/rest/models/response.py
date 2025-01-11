from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.semantic_kernel_sampler.rest.models.request import Request


class Response(BaseModel):
    request: Request = Field()
    id: UUID = Field(init=False)
    message: Optional[str] = Field(default=None)

    def model_post_init(self, **kwargs) -> None:  # type: ignore
        self.id = self.request.id
