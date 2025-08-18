

from semantic_kernel import Kernel

from semantic_kernel_sampler.ai.tooling.typescript_sdk__quick_start.sk.plugin import DemoServerMCPStdioPlugin


class DemoServerKernel(Kernel):

    def __init__(self):
        super().__init__()

        oDemoServerMCPStdioPlugin = DemoServerMCPStdioPlugin()
        self.plugins = [oDemoServerMCPStdioPlugin]  # pyright: ignore[reportAttributeAccessIssue]
