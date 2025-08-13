import asyncio
from typing import TYPE_CHECKING

from flask import Flask, request

from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel

if TYPE_CHECKING:
    from flask.wrappers import Response as FlaskResponse

api: Flask = Flask(__name__)


@api.route("/messages", methods=["POST"])
async def post_async():
    _request: RequestModel = RequestModel.create_from_flask(request)
    print(f"request: {_request}")
    oResponse: ResponseModel = ResponseModel(request=_request)

    # oResponse.message = await semantic-kernel magic
    await asyncio.sleep(1)
    oResponse.message = "Times are tough"

    result: FlaskResponse = oResponse.to_flask()
    return result, 200
