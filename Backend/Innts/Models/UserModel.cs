using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Runtime.Serialization;
using Microsoft.AspNetCore.Identity;
using Newtonsoft.Json;

namespace Innts.Model;

public class CustomUser : IdentityUser<long>
{
    public override long Id { get; set; }
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    [DefaultValue(false)] public bool IsActivate { get; set; }
#pragma warning disable CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
    [JsonIgnore] public override string PasswordHash { get; set; } = string.Empty;
#pragma warning restore CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
    public override string? PhoneNumber { get => base.PhoneNumber; set => base.PhoneNumber = value; }
    [JsonIgnore] public override bool EmailConfirmed { get; set; }
    [JsonIgnore] public override int AccessFailedCount { get; set; }
#pragma warning disable CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
    [JsonIgnore] public override string NormalizedEmail { get; set; } = string.Empty;
#pragma warning restore CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
#pragma warning disable CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
    [JsonIgnore] public override string NormalizedUserName { get; set; } = string.Empty;
#pragma warning restore CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
#pragma warning disable CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
    [JsonIgnore] public override string SecurityStamp { get; set; } = string.Empty;
#pragma warning restore CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
#pragma warning disable CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
    [JsonIgnore] public override string ConcurrencyStamp { get; set; } = Guid.NewGuid().ToString();
#pragma warning restore CS8765 // Nullability of type of parameter doesn't match overridden member (possibly because of nullability attributes).
    [JsonIgnore] public override bool PhoneNumberConfirmed { get; set; }
    [JsonIgnore] public override bool TwoFactorEnabled { get; set; }
    [JsonIgnore] public override bool LockoutEnabled { get; set; }

    [JsonIgnore]
    [IgnoreDataMember][AllowNull] public List<string>? KbDatabaseChache { get; set; } = new List<string>() { "" };
    [JsonIgnore] public CustomUserTokenStorageModel? Token { get; set; }

}
