namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using Microsoft.AspNetCore.Mvc;

    [ApiController]
    [Route("api/[controller]")]
    public abstract class ObservableControllerBase(ILogger<ObservableControllerBase> logger) : ControllerBase
    {
        protected ILogger<ObservableControllerBase> Logger { get; } = logger;
    }
}
