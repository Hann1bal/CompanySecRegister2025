using Newtonsoft.Json;
namespace Innts.Model.Dto;

public class SignUpDto
{
    /// <summary>
    ///     Username
    /// </summary>
    [JsonProperty("userName")]
    public string? Username { get; set; }

    /// <inheritdoc />
    [JsonProperty("email")]
    public required string Email { get; set; }

    /// <inheritdoc />
    [JsonProperty("password")]
    public required string Password { get; set; }

    /// <inheritdoc />
    [JsonProperty("firstName")]
    public string? FirstName { get; set; }

    /// <inheritdoc />
    [JsonProperty("lastName")]
    public string? LastName { get; set; }

    /// <inheritdoc />
    [JsonProperty("databases")]
    public ICollection<long>? Database { get; set; }

    /// <inheritdoc />
    [JsonProperty("roles")]
    public IEnumerable<string>? Roles { get; set; }
}
