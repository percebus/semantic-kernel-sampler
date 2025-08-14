from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import Field

from semantic_kernel_sampler.rest.models.output import OutputModel
from semantic_kernel_sampler.rest.models.request import RequestModel


class ResponseModel(OutputModel):
    # TODO? Use a2a.RequestContext instead?
    request: RequestModel = Field()

    id: UUID = Field(init=False, default_factory=uuid4)

    message: Optional[str] = Field(default=None)

    def model_post_init(self, __context: Any) -> None:  # type: ignore
        self.id = self.request.id
