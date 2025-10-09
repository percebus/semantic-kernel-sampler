"""Configurable mixin for shared components."""

from abc import ABC
from dataclasses import dataclass, field

from agent_framework_sampler.config.configuration import Configuration
from agent_framework_sampler.config.os_environ.settings import Settings


@dataclass
class ConfigurableMixin(ABC):
    """Mixin class to provide configuration and settings access."""

    config: Configuration = field()

    @property
    def settings(self) -> Settings:
        """Returns the settings from the configuration."""
        return self.config.settings
