namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.DependencyInjection
{
    using System.Diagnostics.CodeAnalysis;
    using System.Text.Json;
    using JCystems.SemanticKernelSampler.Dotnet.WebApp.Options;
    using Microsoft.AspNetCore.Http.Json;
    using Microsoft.Extensions.Options;
    using Scrutor;
    using Serilog;

    [ExcludeFromCodeCoverage]
    public static class ServiceRegistrar
    {
        // location of Kubernetes ConfigMap mount within the Pod
        private const string ContainerConfigLocation = "/mnt/app-appSettings-map";
        private const string AppVersion = "1.0.0";

        /// <summary>
        /// Registers services and configures the application.
        /// </summary>
        /// <param name="builder">The <see cref="WebApplicationBuilder"/> to configure.</param>
        /// <returns>The configured <see cref="WebApplicationBuilder"/>.</returns>
        public static WebApplicationBuilder RegisterServices(this WebApplicationBuilder builder)
        {
            builder.Configuration.AddJsonFile("appsettings.json", optional: false);
            builder.Configuration.AddJsonFile("appsettings.ai.json", optional: false, reloadOnChange: true);
            builder.Configuration.AddJsonFile("appsettings.ai.secrets.json", optional: false, reloadOnChange: true);
            builder.Configuration.AddJsonFile("appsettings.Development.json", optional: true, reloadOnChange: true);
            builder.Configuration.AddEnvironmentVariables();

            builder.Services.AddOptions<AppSettingsOptions>()
                .BindConfiguration(AppSettingsOptions.Key)
                .ValidateOnStart();

            var provider = builder.Services.BuildServiceProvider();

            ILoggerFactory loggerFactory = provider.GetRequiredService<ILoggerFactory>();
            Serilog.ILogger logger = Log.ForContext<Program>();

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

            // Add services to the container.
            builder.Services.AddControllers();
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();
            builder.Services.AddHealthChecks();

            // TODO: Add resiliency
            //builder.Services.ConfigureHttpClientDefaults(http =>
            //{
            //    // Turn on resilience by default
            //    http.AddStandardResilienceHandler();
            //});


            builder.Services.Configure<JsonOptions>(oJsonOptions =>
            {
                JsonSerializerOptions oJsonSerializerOptions = oJsonOptions.SerializerOptions;
                oJsonSerializerOptions.PropertyNameCaseInsensitive = false;
                oJsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
            });


            builder.Services.Scan(
                s => s.FromAssemblyOf<Program>()
                      .AddClasses()
                      .UsingRegistrationStrategy(RegistrationStrategy.Skip)
                      .AsMatchingInterface());

            return builder;
        }
    }
}
