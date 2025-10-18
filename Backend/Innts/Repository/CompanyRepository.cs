using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Innts.Context;
using Innts.Models;
using Microsoft.EntityFrameworkCore;
namespace Innts.Repository;

public class CompanyRepository : IBaseRepository<CompanyModel>
{
    private readonly IDbContextFactory<DatabaseContext> _factory;
    public CompanyRepository(IDbContextFactory<DatabaseContext> factory)
    {
        _factory = factory;
    }
    public async Task<bool> Add(CompanyModel item)
    {
        await using var context = await _factory.CreateDbContextAsync();
        await context.Companies.AddAsync(item);
        await context.SaveChangesAsync();
        return true;
    }
    public async void AddList(List<CompanyModel> item)
    {
        await using var context = await _factory.CreateDbContextAsync();
        await context.Companies.AddRangeAsync(item);
        await context.SaveChangesAsync();
    }
    public async Task<CompanyModel> FindById(long id, string ids)
    {
        await using var context = await _factory.CreateDbContextAsync();
        return await context.Companies.FirstAsync(x => x.inn == id);
    }
    public async Task<CompanyModel> FindByIdAsync(long id, string ids)
    {
        await using var context = await _factory.CreateDbContextAsync();
        return await context.Companies.FirstAsync(x => x.orgName == ids);
    }
    public List<CompanyModel> GetAll()
    {
        using var context = _factory.CreateDbContext();
        return context.Companies.ToList();
    }
    public async void Remove(int id)
    {
        await using var context = await _factory.CreateDbContextAsync();
        var timeSpan = DateTime.UtcNow - new DateTime(1970, 1, 1, 0, 0, 0, 0);
        var db = context.Companies.FirstOrDefault(c => c.Id == id);
        if (db == null) return;
        context.Companies.Remove(db);
        context.SaveChanges();
    }
    public void Restore(int id)
    {
        throw new NotImplementedException();
    }
    public async void Update(CompanyModel item)
    {
        await using var context = await _factory.CreateDbContextAsync();

        context.Companies.Update(item);
        await context.SaveChangesAsync();
    }
    public async void UpdateList(List<CompanyModel> item)
    {
        await using var context = await _factory.CreateDbContextAsync();
        context.Companies.UpdateRange(item);
        await context.SaveChangesAsync();
    }

}

