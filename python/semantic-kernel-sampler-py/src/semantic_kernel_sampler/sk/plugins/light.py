# Copyright (c) Microsoft. All rights reserved.

from typing import Annotated

from semantic_kernel.functions import kernel_function

from semantic_kernel_sampler.sk.plugins.protocol import PluginProtocol


# SRC: https://github.com/microsoft/semantic-kernel/blob/40734345dcb5be298d524f58b5d3bf2afd835f27/python/samples/learn_resources/plugin.py#L11
class LightPlugin(PluginProtocol):
    is_on: bool = False

    @kernel_function(
        name="get_state",
        description="Gets the state of the light.",
    )
    def get_state(
        self,
    ) -> Annotated[str, "the output is a string"]:
        """Returns the state result of the light."""
        return "On" if self.is_on else "Off"

    @kernel_function(
        name="change_state",
        description="Changes the state of the light.",
    )
    def change_state(
        self,
        new_state: Annotated[bool, "the new state of the light"],
    ) -> Annotated[str, "the output is a string"]:
        """Changes the state of the light."""
        self.is_on = new_state
        state = self.get_state()
        print(f"The light is now: {state}")
        return state
