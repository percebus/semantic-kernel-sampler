namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using Azure.ResourceManager.ApiManagement;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.Extensions.Logging;

    public class ProductController(ILogger<ObservableControllerBase> logger, ServiceProductApiLinkCollection apis) : ObservableControllerBase(logger)
    {
        public ServiceProductApiLinkCollection Apis { get; } = apis;

        [HttpGet]
        public async Task<IActionResult> GetAllProductApisAsync()
        {
            var contracts = new List<ServiceProductApiLinkResource>();

            // SRC: https://github.com/Azure/azure-sdk-for-net/blob/Azure.ResourceManager.ApiManagement_1.3.0/sdk/apimanagement/Azure.ResourceManager.ApiManagement/tests/Generated/Samples/Sample_ServiceProductApiLinkCollection.cs
            await foreach (ServiceProductApiLinkResource item in this.Apis.GetAllAsync())
            {
                contracts.Add(item);
            }

            IEnumerable<string> apiIds = contracts.Select(o => o.Data.ApiId);
            return this.Ok(apiIds);
        }
    }
}
