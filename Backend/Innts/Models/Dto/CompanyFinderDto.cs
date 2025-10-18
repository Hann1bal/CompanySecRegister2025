using System.Text.Json.Serialization;

namespace Innts.Model.Dto;

public class CompanyFinderDto
{
    [JsonPropertyName("inn")]
    public string? INN { get; set; }
    [JsonPropertyName("name")]
    public string? CompanyName { get; set; }
}