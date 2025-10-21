using JCystems.AgentFraweworkSampler.DotNet.WebApp.Extensions.WebApplicationBuilder;

var builder = WebApplication.CreateBuilder(args);

// NOTE: See <see cref="Extensions/WebApplicationBuilder/DependencyInjection.cs"/> for more details
builder.RegisterServices();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();

    // Add OpenAPI 3.0 document serving middleware
    // Available at: http://localhost:<port>/swagger/v1/swagger.json
    app.UseOpenApi();

    // Add web UIs to interact with the document
    // Available at: http://localhost:<port>/swagger
    app.UseSwaggerUi(); // UseSwaggerUI Protected by if (env.IsDevelopment())
}

// TODO Move to appSettings.json
string? isDotNETRunningInContainer = Environment.GetEnvironmentVariable("DOTNET_RUNNING_IN_CONTAINER");

// Only use HTTPS redirection when not running in a container
if (string.IsNullOrEmpty(isDotNETRunningInContainer))
{
    app.UseHttpsRedirection();
}
else
{
    // Skip HTTPS redirection in containers
}

app.UseAuthorization();

app.MapControllers();

app.Run();
