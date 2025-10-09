from lagom import Container

from agent_framework._clients import BaseChatClient
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient


container = Container()

container[AzureCliCredential] = AzureCliCredential
container[AzureOpenAIChatClient] = lambda c: AzureOpenAIChatClient(credential=c[AzureCliCredential])
container[BaseChatClient] = lambda c: c[AzureOpenAIChatClient]
