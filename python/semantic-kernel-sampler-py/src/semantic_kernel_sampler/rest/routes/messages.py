from typing import TYPE_CHECKING, Optional

from flask import Flask, request
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.contents import ChatHistory

from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel

if TYPE_CHECKING:
    from flask.wrappers import Response as FlaskResponse
    from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
    from semantic_kernel.contents.chat_message_content import ChatMessageContent


api: Flask = Flask(__name__)


@api.route("/messages", methods=["GET"])
async def get_async():
    return "Right place, wrong method"


@api.route("/messages", methods=["POST"])
async def post_async():
    _request: RequestModel = RequestModel.create_from_flask(request)
    print(f"request: {_request}")

    oChatHistory: ChatHistory = container[ChatHistory]
    oChatHistory.add_user_message(_request.message)

    oKernel: Kernel = container[Kernel]
    oPromptExecutionSettings: PromptExecutionSettings = container[AzureChatPromptExecutionSettings]
    oPromptExecutionSettings.function_choice_behavior = FunctionChoiceBehavior.Auto()  # type: ignore # XXX FIXME

    oResponse: ResponseModel = ResponseModel(request=_request)
    oAzureChatCompletion: AzureChatCompletion = container[AzureChatCompletion]

    oChatMessageContent: Optional[ChatMessageContent] = await oAzureChatCompletion.get_chat_message_content(
        kernel=oKernel, settings=oPromptExecutionSettings, chat_history=oChatHistory
    )

    if oChatMessageContent:
        oResponse.message = str(oChatMessageContent)
        oChatHistory.add_assistant_message(oResponse.message)

    result: FlaskResponse = oResponse.to_flask()
    return result, 200
