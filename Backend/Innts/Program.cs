using System.Diagnostics;
using System.Text;
using Innts.Context;
using Innts.Models;
using Innts.Repository;
using Innts.Services;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Innts.Repository;     // если CompanyRepository там
using Innts.Models;           // если CompanyModel там
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;


var builder = WebApplication.CreateBuilder(args);

var originSpecificName = "unbaned";
builder.Services.AddCors(options =>
{
    options.AddPolicy(originSpecificName,
        policy =>
        {
            policy.AllowAnyOrigin()
                    .AllowAnyMethod()
                    .AllowAnyHeader();

        });
    options.AddPolicy(originSpecificName,
        builder =>
        {
            builder
            .WithOrigins("https://localhost", "https://localhost:5173", "http://localhost:4000", "localhost:4000")
            .AllowCredentials()
            .AllowAnyMethod()
            .AllowAnyHeader();
        }
    );
});
builder.Services.AddControllers();
builder.Services.AddHttpClient("httos", config =>
{
    config.BaseAddress = new Uri(builder.Configuration.GetSection("KbAuthProperty")["baseUri"]!);
    config.Timeout = new TimeSpan(0, 0, 30);
    config.DefaultRequestHeaders.Clear();
});
builder.Services.AddScoped<IFileService, FileService>();
builder.Services.AddSingleton<HttpClientService>();
builder.Services.AddSingleton<TestService>();
builder.Services.AddDbContextFactory<DatabaseContext>
(
    optionsBuilder =>
    {
        optionsBuilder.UseNpgsql(DatabaseContext.GetDatabaseConnectionString(builder.Configuration));
        optionsBuilder.EnableDetailedErrors(false);
        optionsBuilder.EnableSensitiveDataLogging(false);

    }
);
builder.Services.AddScoped<IBaseRepository<CompanyModel>, CompanyRepository>();
builder.Services.AddHostedService<TimedService>();
builder.Services.AddEndpointsApiExplorer();


builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.SaveToken = true;
    options.RequireHttpsMetadata = false;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidIssuer = builder.Configuration.GetSection("Tokens")["Issuer"],
        ValidAudience = builder.Configuration.GetSection("Tokens")["Audience"],
        ValidateLifetime = true,
        RequireExpirationTime = false,
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration.GetSection("Tokens")["Key"]!)),
        ValidateIssuerSigningKey = true,
        ClockSkew = TimeSpan.Zero
    };


    options.Events = new JwtBearerEvents
    {

        OnAuthenticationFailed = context =>
        {
            if (context.Exception.GetType() == typeof(SecurityTokenExpiredException))
                context.Response.Headers["Token-Expired"] = "true";
            return Task.CompletedTask;
        },
        OnMessageReceived = context =>
        {
            var accessToken = context.Request.Query["access_token"];
            // If the request is for our hub...
            var path = context.HttpContext.Request.Path;
            if (!string.IsNullOrEmpty(accessToken) && path.StartsWithSegments("/KbEditor"))
            {
                // Read the token out of the query string
                context.Token = accessToken;
            }
            return Task.CompletedTask;
        }
    };
});


// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

var app = builder.Build();
//app.MapOpenApi();
// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapGet("/", () => Results.Redirect("/openapi/v1.json"));
}
app.UseAuthentication();
app.UseCors(originSpecificName);
app.UseRouting();
app.UseAuthorization();
app.MapControllers();
app.Run();

