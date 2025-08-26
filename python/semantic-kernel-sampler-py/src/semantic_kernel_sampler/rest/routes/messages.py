from typing import TYPE_CHECKING, Optional

from flask import Flask, request
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel
from semantic_kernel_sampler.sk.invokers.custom.chat.invoker import CustomSemanticChatInvoker

if TYPE_CHECKING:
    from flask.wrappers import Response as FlaskResponse
    from semantic_kernel.contents.kernel_content import KernelContent


api: Flask = Flask(__name__)


@api.route("/messages", methods=["GET"])
async def get_async():
    return "Right place, wrong method"


@api.route("/messages", methods=["POST"])
async def post_async():
    _request: RequestModel = RequestModel.create_from_flask(request)
    print(f"request: {_request}")

    oCustomSemanticChatInvoker: CustomSemanticChatInvoker = container[CustomSemanticChatInvoker]

    oResponse: ResponseModel = ResponseModel(request=_request)

    requestChatMessageContent = ChatMessageContent(role=AuthorRole.USER, content=_request.message)
    messages: list[KernelContent] = [requestChatMessageContent]

    responseChatMessageContent: Optional[KernelContent] = await oCustomSemanticChatInvoker.invoke(messages=messages)
    if responseChatMessageContent:
        oResponse.message = str(responseChatMessageContent)

    result: FlaskResponse = oResponse.to_flask()
    return result, 200
