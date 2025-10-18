
using Innts.Context;
using Innts.Models;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;

public class TimedService(IDbContextFactory<DatabaseContext> dbContextFactory, HttpClientService httpClientService) : IHostedService, IDisposable
{
    public IDbContextFactory<DatabaseContext> DbContextFactory = dbContextFactory;
    private readonly TimeSpan _syncInterval = TimeSpan.FromMinutes(60); // Интервал синхронизации
    private Timer _timer = null!;
    private readonly HttpClientService _httpClientService = httpClientService;
    public async Task SyncDb(object? state)
    {
        var context = await DbContextFactory.CreateDbContextAsync();
        var result = await _httpClientService.GetAsync("{0}/api/v1/companies?page=1&size=50");
        var companies = JsonConvert.DeserializeObject<List<CompanyModel>>(result);
        var toInsert = new List<CompanyModel>();
        var toUpdate = new List<CompanyModel>();

        foreach (var company in companies)
        {
            var existingEntity = await context.Companies.FirstOrDefaultAsync(x => x.inn == company.inn);

            if (existingEntity == null)
            {
                toInsert.Add(existingEntity);
            }
            else
            {
                toUpdate.Add(existingEntity);
            }

        }
        if (toInsert.Any())
        {
            await context.Companies.AddRangeAsync(toInsert);
        }

        if (toUpdate.Any())
        {
            context.Companies.UpdateRange(toUpdate);
        }
        await context.SaveChangesAsync();
    }
    public async Task StartAsync(CancellationToken cancellationToken)
    {
        _timer = new Timer(async o => await SyncDb(o), null, TimeSpan.Zero, _syncInterval);
    }

    public async Task StopAsync(CancellationToken cancellationToken)
    {
        _timer?.Change(Timeout.Infinite, 0);
    }

    public void Dispose()
    {
        _timer?.Dispose();
    }

}