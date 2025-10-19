
using Innts.Context;
using Innts.Models;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class TimedService(IDbContextFactory<DatabaseContext> dbContextFactory, HttpClientService httpClientService) : IHostedService, IDisposable
{
    public IDbContextFactory<DatabaseContext> DbContextFactory = dbContextFactory;
    private readonly TimeSpan _syncInterval = TimeSpan.FromMinutes(60); // Интервал синхронизации
    private Timer _timer = null!;
    private readonly HttpClientService _httpClientService = httpClientService;
public async Task SyncDb(object? state)
{
    var context = await DbContextFactory.CreateDbContextAsync();

    // Получаем JSON с API
    var result = await _httpClientService.GetAsync("{0}/api/v1/companies?page=1&size=100");

    // Разбираем ответ
    var json = JObject.Parse(result);
    var companies = json["companies"]?.ToObject<List<JObject>>() ?? new();

    var toInsert = new List<CompanyModel>();
    var toUpdate = new List<CompanyModel>();

    foreach (var c in companies)
    {
        string inn = c["inn"]?.ToString() ?? string.Empty;
        if (string.IsNullOrEmpty(inn))
            continue;

        var existingEntity = await context.Companies.FirstOrDefaultAsync(x => x.inn == inn);

        var mapped = new CompanyModel
        {
            inn = inn,
            orgName = c["name"]?.ToString() ?? string.Empty,
            orgFullName = c["full_name"]?.ToString() ?? string.Empty,
            status = c["status"]?.ToString() ?? string.Empty,
            legalAddress = c["legal_address"]?.ToString() ?? string.Empty,
            mainOkved = c["main_okved"]?.ToString() ?? string.Empty,
            okved_description = c["okved_description"]?.ToString(),
            registrationDate = c["registration_date"]?.ToString(),
            director = c["director"]?.ToString(),
            website = c["website"]?.ToString(),
            email = c["email"]?.ToString(),
            create_at = DateTime.TryParse(c["created_at"]?.ToString(), out var createdAt) ? createdAt : DateTime.Now,
            update_at = DateTime.TryParse(c["updated_at"]?.ToString(), out var updatedAt) ? updatedAt : DateTime.Now
        };

        if (existingEntity == null)
        {
            toInsert.Add(mapped);
        }
        else
        {
            // Обновляем только нужные поля
            existingEntity.orgName = mapped.orgName;
            existingEntity.orgFullName = mapped.orgFullName;
            existingEntity.status = mapped.status;
            existingEntity.legalAddress = mapped.legalAddress;
            existingEntity.mainOkved = mapped.mainOkved;
            existingEntity.okved_description = mapped.okved_description;
            existingEntity.registrationDate = mapped.registrationDate;
            existingEntity.director = mapped.director;
            existingEntity.website = mapped.website;
            existingEntity.email = mapped.email;
            existingEntity.update_at = DateTime.Now;

            toUpdate.Add(existingEntity);
        }
    }

    if (toInsert.Any())
        await context.Companies.AddRangeAsync(toInsert);

    if (toUpdate.Any())
        context.Companies.UpdateRange(toUpdate);

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