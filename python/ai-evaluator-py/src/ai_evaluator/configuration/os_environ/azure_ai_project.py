


from pydantic import BaseModel


class  AzureAIProjectSettings(BaseModel):
    subscription_id: str

    resource_group_name: str

    endpoint: str

    project_name: str
