namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Extensions.WebApplicationBuilder
{
    using System.ClientModel;
    using System.Diagnostics.CodeAnalysis;
    using System.Text.Json;
    using Azure;
    using Azure.AI.OpenAI;
    using Azure.Core;
    using Azure.Identity;
    using Azure.ResourceManager;
    using Azure.ResourceManager.ApiManagement;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Options;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Services;
    using Microsoft.Agents.CopilotStudio.Client;
    using Microsoft.AspNetCore.Http.Json;
    using Microsoft.Extensions.AI;
    using Microsoft.Extensions.DependencyInjection.Extensions;
    using Microsoft.Extensions.Options;
    using Microsoft.SemanticKernel;
    using Microsoft.SemanticKernel.Agents;
    using Microsoft.SemanticKernel.Agents.Copilot;
    using Microsoft.SemanticKernel.ChatCompletion;
    using Scrutor;
    using Serilog;


    [ExcludeFromCodeCoverage]
    public static class DependencyInjection
    {
        public static Microsoft.AspNetCore.Builder.WebApplicationBuilder RegisterServices(this Microsoft.AspNetCore.Builder.WebApplicationBuilder builder)
        {
            builder.Configuration.AddJsonFile("appsettings.json", optional: false);
            builder.Configuration.AddJsonFile("appsettings.ai.json", optional: false, reloadOnChange: true);
            builder.Configuration.AddJsonFile("appsettings.copilotstudio.json", optional: false, reloadOnChange: true);
            builder.Configuration.AddJsonFile("appsettings.Development.json", optional: true, reloadOnChange: true);
            builder.Configuration.AddEnvironmentVariables();

            builder.Services.AddOptions<AppSettingsOptions>()
                .BindConfiguration(AppSettingsOptions.Key)
                .ValidateDataAnnotations()
                .ValidateOnStart();

            var provider = builder.Services.BuildServiceProvider();

            ILogger logger = Log.ForContext<Program>();

            AppSettingsOptions appSettings;
            try
            {
                // this gets us a copy of appSettings to use at startup
                appSettings = provider.GetRequiredService<IOptionsMonitor<AppSettingsOptions>>().CurrentValue;
            }
            catch (Exception ex)
            {
                logger.Fatal(ex, "Invalid configuration, please verify that your configuration is correct. Error: {ex}", ex.Message);
                throw;
            }

            builder.Services.TryAddSingleton<DefaultAzureCredential>(provider => new(
                new DefaultAzureCredentialOptions()
                {
                    // Exclude credentials that often fail with CA policies
                    ExcludeSharedTokenCacheCredential = true,
                    ExcludeInteractiveBrowserCredential = true,
                    ExcludeAzurePowerShellCredential = true,

                    // Keep these for development
                    ExcludeAzureCliCredential = false,
                    ExcludeVisualStudioCredential = false,
                    ExcludeVisualStudioCodeCredential = false,
                    ExcludeManagedIdentityCredential = false,
                }));

            builder.Services.TryAddSingleton<ClientSecretCredential>(provider =>
            {
                AzureCredentialOptions oAzureCredentialOptions = appSettings.AzureCredential;
                return new(
                    oAzureCredentialOptions.TenantId,
                    oAzureCredentialOptions.ClientId,
                    oAzureCredentialOptions.ClientSecret);
            });

            builder.Services.TryAddSingleton<TokenCredential>(provider =>
            {
                // NOTE: Choose either or
                // return provider.GetRequiredService<DefaultAzureCredential>();
                return provider.GetRequiredService<ClientSecretCredential>();
            });

            builder.Services.TryAddSingleton<ArmClient>(provider =>
            {
                var oTokenCredential = provider.GetRequiredService<TokenCredential>();
                return new(oTokenCredential);
            });


            builder.Services.TryAddSingleton<ApiManagementServiceResource>(provider =>
            {
                AzureApiMProductOptions oApiMProductOptions = appSettings.AzureApiMProduct;
                var oResourceIdentifier = ApiManagementServiceResource.CreateResourceIdentifier(
                        oApiMProductOptions.SubscriptionId,
                        oApiMProductOptions.ResourceGroupName,
                        oApiMProductOptions.ServiceName);

                return provider
                    .GetRequiredService<ArmClient>()
                    .GetApiManagementServiceResource(oResourceIdentifier);
            });

            // SRC: // SRC: https://github.com/Azure/azure-sdk-for-net/blob/Azure.ResourceManager.ApiManagement_1.3.0/sdk/apimanagement/Azure.ResourceManager.ApiManagement/tests/Generated/Samples/Sample_ServiceProductApiLinkCollection.cs
            builder.Services.TryAddSingleton<ApiManagementProductResource>(provider =>
            {
                AzureApiMProductOptions oApiMProductOptions = appSettings.AzureApiMProduct;
                var oResourceIdentifier = ApiManagementProductResource.CreateResourceIdentifier(
                        oApiMProductOptions.SubscriptionId,
                        oApiMProductOptions.ResourceGroupName,
                        oApiMProductOptions.ServiceName,
                        oApiMProductOptions.ProductId);

                return provider
                    .GetRequiredService<ArmClient>()
                    .GetApiManagementProductResource(oResourceIdentifier);
            });

            builder.Services.TryAddSingleton<ApiCollection>(provider =>
            {
                return provider
                    .GetRequiredService<ApiManagementServiceResource>()
                    .GetApis();
            });

            // Add APIM Subscription Resource to get subscription keys
            builder.Services.TryAddSingleton<ApiManagementSubscriptionResource>(provider =>
            {
                AzureApiMProductOptions oApiMProductOptions = appSettings.AzureApiMProduct;
                AzureCredentialOptions oAzureCredentialOptions = appSettings.AzureCredential;
                
                // Use the ClientId from AzureCredential as the subscription ID in APIM
                var oResourceIdentifier = ApiManagementSubscriptionResource.CreateResourceIdentifier(
                        oApiMProductOptions.SubscriptionId,
                        oApiMProductOptions.ResourceGroupName,
                        oApiMProductOptions.ServiceName,
                        oAzureCredentialOptions.ClientId); // This is your APIM subscription ID

                return provider
                    .GetRequiredService<ArmClient>()
                    .GetApiManagementSubscriptionResource(oResourceIdentifier);
            });

            // Add service to retrieve APIM subscription keys
            builder.Services.TryAddScoped<Func<Task<string>>>(provider => async () =>
            {
                var subscriptionResource = provider.GetRequiredService<ApiManagementSubscriptionResource>();
                var subscriptionKeys = await subscriptionResource.GetSecretsAsync();
                return subscriptionKeys.Value.PrimaryKey; // or SecondaryKey
            });

            builder.Services.TryAddSingleton<FunctionChoiceBehavior>(FunctionChoiceBehavior.Auto());
            builder.Services.TryAddSingleton<PromptExecutionSettings>(provider =>
            {
                var oFunctionChoiceBehavior = provider.GetRequiredService<FunctionChoiceBehavior>();
                return new()
                {
                    FunctionChoiceBehavior = oFunctionChoiceBehavior,
                };
            });

            // SRC: https://github.com/microsoft/semantic-kernel/blob/dotnet-1.64.0/dotnet/samples/Concepts/Agents/ChatCompletion_ServiceSelection.cs
            builder.Services.TryAddScoped<ApiKeyCredential>(provider => new AzureKeyCredential(appSettings.AiModel.ApiKey));
            builder.Services.TryAddScoped<AzureOpenAIClient>(provider =>
            {
                var oApiKeyCredential = provider.GetRequiredService<ApiKeyCredential>();
                return new(appSettings.AiModel.Endpoint, oApiKeyCredential);
            });

            builder.Services.TryAddScoped<ChatHistory>(provider =>
            {
                // TODO: Add System Message
                return new();
            });

            builder.Services.AddTransient<IChatClient>(provider => provider
                .GetRequiredService<AzureOpenAIClient>()
                .GetChatClient(appSettings.AiModel.DeploymentId)
                .AsIChatClient());

            builder.Services.TryAddTransient<IKernelBuilder>(provider => Kernel.CreateBuilder());

            builder.Services.TryAddTransient<Kernel>(provider =>
            {
                var oKernelBuilder = provider.GetRequiredService<IKernelBuilder>();
                var oAzureOpenAIClient = provider.GetRequiredService<AzureOpenAIClient>();

                // NOTE: Chose 1 or the other?
                oKernelBuilder.AddAzureOpenAIChatClient(appSettings.AiModel.DeploymentId, oAzureOpenAIClient);
                // oKernelBuilder.AddAzureOpenAIChatCompletion(appSettings.AiModel.DeploymentId, oAzureOpenAIClient);

                // oKernelBuilder.Plugins.AddFromType<YourTypeHere>(); // TODO: Add your plugins here

                return oKernelBuilder.Build();
            });

            builder.Services.TryAddTransient<IChatCompletionService>(provider => provider
                .GetRequiredService<Kernel>()
                .GetRequiredService<IChatCompletionService>());

            builder.Services.TryAddTransient<ChatCompletionAgent>(provider =>
            {
                var oKernel = provider.GetRequiredService<Kernel>();
                return new()
                {
                    Name = "ChatCompletionAgent",
                    Instructions = "You are a helpful AI assistant.",
                    Kernel = oKernel,
                };
            });

#pragma warning disable SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.
            builder.Services.TryAddSingleton<CopilotStudioConnectionSettings>(provider => new(
                appSettings.CopilotStudio.TenantId,
                appSettings.CopilotStudio.ClientId,
                appSettings.CopilotStudio.ClientSecret)
            {
                EnvironmentId = appSettings.CopilotStudio.EnvironmentId,
                SchemaName = appSettings.CopilotStudio.SchemaName,
            });

            builder.Services.TryAddScoped<CopilotClient>(provider =>
            {
                var oCopilotStudioConnectionSettings = provider.GetRequiredService<CopilotStudioConnectionSettings>();
                return CopilotStudioAgent.CreateClient(oCopilotStudioConnectionSettings);
            });

            builder.Services.TryAddTransient<CopilotStudioAgent>(provider =>
            {
                var oCopilotClient = provider.GetRequiredService<CopilotClient>();
                return new(oCopilotClient);
            });

            // builder.Services.TryAddTransient<Agent>(provider => provider.GetRequiredService<ChatCompletionAgent>());
            builder.Services.TryAddTransient<Agent>(provider => provider.GetRequiredService<CopilotStudioAgent>());
#pragma warning restore SKEXP0110 // Type is for evaluation purposes only and is subject to change or removal in future updates. Suppress this diagnostic to proceed.

            // SRC: https://github.com/microsoft/semantic-kernel/blob/main/dotnet/samples/GettingStartedWithAgents/A2A/Step01_A2AAgent.cs
            builder.Services.TryAddTransient<HttpClientHandler>();
            // builder.Services.TryAddTransient<LoggingHandler>(); // FIXME
            builder.Services.TryAddScoped<HttpClient>(provider =>
            {
                var oHttpClientFactory = provider.GetRequiredService<IHttpClientFactory>();
                // var oLoggingHandler = provider.GetRequiredService<LoggingHandler>(); // FIXME
                return oHttpClientFactory.CreateClient();
            });

            // XXX dynamic from APIM + APIC
            builder.Services.TryAddScoped<IA2AService>(provider =>
            {
                // FIXME read from Options
                Uri baseURI = new Uri("http://localhost:9999"); // /.well-known/agent-card.json");
                var oHttpClient = provider.GetRequiredService<HttpClient>();
                return new A2AService(oHttpClient, baseURI);
            });

            builder.Services.Scan(
                s => s.FromAssemblyOf<Program>()
                      .AddClasses()
                      .UsingRegistrationStrategy(RegistrationStrategy.Skip)
                      .AsMatchingInterface());

            builder.Services.TryAddTransient<ICustomChatAgent, CustomChatAgent>();

            // Add services to the container.
            builder.Services.AddControllers();
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();
            builder.Services.AddHealthChecks();

            // Add HTTP client for A2A communication
            builder.Services.AddHttpClient();

            // TODO: Add resiliency
            // builder.Services.ConfigureHttpClientDefaults(http =>
            // {
            //     // Turn on resilience by default
            //     http.AddStandardResilienceHandler();
            // });

            builder.Services.Configure<JsonOptions>(oJsonOptions =>
            {
                JsonSerializerOptions oJsonSerializerOptions = oJsonOptions.SerializerOptions;
                oJsonSerializerOptions.PropertyNameCaseInsensitive = false;
                oJsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
            });

            return builder;
        }
    }
}
