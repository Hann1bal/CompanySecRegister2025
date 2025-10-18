using Newtonsoft.Json;

namespace Innts.Model.Dto;

public class AuthUserDto
{
    [JsonProperty("userName")] public string Username { get; set; } = string.Empty;
    [JsonProperty("email")] public string Email { get; set; } = string.Empty;
    [JsonProperty("roles")] public IEnumerable<string> Roles { get; set; } = [];
    [JsonProperty("isActivate")] public bool IsActivate { get; set; }
}
