namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Controllers
{
    using Azure.ResourceManager.ApiManagement;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.Extensions.Logging;

    public class ApiMController(ILogger<ObservableControllerBase> logger, ApiCollection apis) : ObservableControllerBase(logger)
    {
        public ApiCollection Apis { get; } = apis;

        [HttpGet]
        public async Task<IActionResult> GetAllApisAsync()
        {
            var contracts = new List<ApiResource>();

            // SRC: https://github.com/Azure/azure-sdk-for-net/blob/Azure.ResourceManager.ApiManagement_1.3.0/sdk/apimanagement/Azure.ResourceManager.ApiManagement/tests/Generated/Samples/Sample_ServiceProductApiLinkCollection.cs
            await foreach (ApiResource item in this.Apis.GetAllAsync())
            {
                contracts.Add(item);
            }

            return this.Ok(contracts);
        }
    }
}
