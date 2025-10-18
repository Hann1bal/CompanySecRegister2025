using Innts.Model;
using Innts.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Npgsql;

namespace Innts.Context;

public class DatabaseContext : IdentityDbContext<CustomUser, IdentityRole<long>, long>
{
    public readonly IConfiguration _configuration;
    public DatabaseContext(DbContextOptions<DatabaseContext> options, IConfiguration configuration) : base(options)
    {
        _configuration = configuration;
    }

    public override DbSet<CustomUser> Users { get; set; }
    public DbSet<CustomUserTokenStorageModel> TokenStorage { get; set; }
    public DbSet<CompanyModel> Companies { get; set; }

    public static string GetDatabaseConnectionString(IConfiguration _configuration)
    {
        var port = int.TryParse(_configuration["DataBase:port"], out var result);
        return new NpgsqlConnectionStringBuilder
        {
            Host = _configuration["DataBase:host"],
            Port = result,
            Database = _configuration["DataBase:database"],
            Username = _configuration["DataBase:username"],
            Password = _configuration["DataBase:password"],
        }.ConnectionString;
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
    }

}