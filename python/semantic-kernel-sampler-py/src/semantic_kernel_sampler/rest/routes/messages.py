import asyncio

from flask import Flask, jsonify, request

from src.semantic_kernel_sampler.rest.models.request import Request
from src.semantic_kernel_sampler.rest.models.response import Response

api: Flask = Flask(__name__)


@api.route("/messages", methods=["POST"])
async def post_async():
    body = request.get_json()
    _request: Request = Request(**body)
    print(f"request: {_request}")
    oResponse: Response = Response(request=_request)

    # oResponse.message = await semantic-kernel magic
    await asyncio.sleep(1)
    return jsonify(oResponse)
