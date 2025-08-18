

from semantic_kernel import Kernel

from semantic_kernel_sampler.ai.tooling.math.sk.plugin import MathPlugin


class MathKernel(Kernel):

    def __init__(self):
        super().__init__()

        oMathPlugin = MathPlugin()
        self.plugins = [oMathPlugin]  # pyright: ignore[reportAttributeAccessIssue]
