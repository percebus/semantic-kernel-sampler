"""Shared Configuration Module."""

from typing import Any, Optional

from pydantic import BaseModel, Field

from semantic_kernel_sampler.configuration.os_environ.settings import Settings


class Config(BaseModel):
    """Shared configuration model for the application."""

    settings: Settings = Field(default_factory=Settings)  # type: ignore[assignment]  # FIXME

    @property
    def debug(self) -> bool:
        """Return True if the environment is 'dev' or 'test', otherwise False."""
        return self.settings.debug

    def safe_model_dump(self) -> Optional[dict[str, Any]]:
        """Safely dump the model to a dictionary, ignoring any errors."""
        return self.settings.model_dump() if self.settings.debug else None
