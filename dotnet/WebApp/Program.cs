using JCystems.SemanticKernelSampler.Dotnet.WebApp.ExtensionMethods;

var builder = WebApplication.CreateBuilder(args);

// NOTE: See <see cref="DependencyInjection/ServiceRegistrar.cs"/> for more details
builder.RegisterServices();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
