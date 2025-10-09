from lagom import Container

from agent_framework._clients import BaseChatClient
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient


container = Container()

container[AzureOpenAIChatClient] = AzureOpenAIChatClient
container[BaseChatClient] = lambda c: c[AzureOpenAIChatClient]
container[AzureCliCredential] = AzureCliCredential
