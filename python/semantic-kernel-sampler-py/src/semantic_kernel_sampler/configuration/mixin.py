"""Configurable mixin for shared components."""

from dataclasses import dataclass, field

from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.configuration.os_environ.settings import Settings


@dataclass
class ConfigurableMixin:
    """Mixin class to provide configuration and settings access."""

    config: Config = field()

    @property
    def settings(self) -> Settings:
        """Returns the settings from the configuration."""
        return self.config.settings
