
from semantic_kernel import Kernel

from semantic_kernel_sampler.ai.tooling.light.sk.plugin import LightPlugin


class LightKernel(Kernel):

    def __init__(self):
        super().__init__()

        oLightPlugin = LightPlugin()
        self.plugins = [oLightPlugin]  # pyright: ignore[reportAttributeAccessIssue]
