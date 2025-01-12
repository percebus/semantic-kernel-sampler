namespace JCystems.SemanticKernelSampler.Dotnet.WebApp.Models
{
    public class Response
    {
        public Guid Id { get; set; } = Guid.Empty;

        public string? Message { get; set; } = null;

        private Request request = null!;
        public required Request Request
        {
            set
            {
                this.request = value;
                this.Id = value.Id;
            }

            get => this.request;
        }
    }
}
