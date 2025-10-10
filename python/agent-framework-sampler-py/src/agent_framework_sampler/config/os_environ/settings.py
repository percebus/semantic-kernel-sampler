""".env os.environ ENVIRONMENT VARIABLES settings module."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from agent_framework_sampler.config.os_environ.a2a import A2ASettings
from agent_framework_sampler.config.os_environ.azure_openai import AzureOpenAISettings


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
    a2a: A2ASettings = Field(default_factory=A2ASettings)

    multi_agent_delimiter: str = Field(default="\n\n---\n\nNEW CONVERSATION\n\n---\n\n")
