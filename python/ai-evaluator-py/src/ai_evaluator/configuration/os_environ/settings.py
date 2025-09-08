""".env os.environ ENVIRONMENT VARIABLES settings module."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from ai_evaluator.configuration.os_environ.azure_ai_project import AzureAIProjectSettings
from ai_evaluator.configuration.os_environ.azure_openai import AzureOpenAISettings


class Settings(BaseSettings):
    """Base class for settings."""

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_prefix="",
        env_nested_delimiter="__",
    )

    debug: bool = Field(default=False)
    dry_run: bool = Field(default=True)
    environment: str = Field(min_length=2)

    azure_openai: AzureOpenAISettings = Field(default_factory=AzureOpenAISettings)  # type: ignore[assignment]  # FIXME

    # Option A): Azure AI Hub
    azure_ai_project: Optional[AzureAIProjectSettings] = Field(default_factory=AzureAIProjectSettings)  # type: ignore[assignment]  # FIXME

    # Option B): Azure AI Foundry Connection
    azure_ai_project_endpoint: Optional[str] = Field(default=None)
