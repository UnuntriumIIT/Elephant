using Microsoft.Extensions.DependencyInjection;

namespace services
{
    public static class TodoListServicesExtensions
    {
        public static IServiceCollection AddImgList(this IServiceCollection serviceCollection)
        {
            return serviceCollection.AddScoped<IDbService, DbService>();
        }
    }
}
