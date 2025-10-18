namespace Innts.Model.Dto;

public class RefreshTokenDto
{
    public required string RefreshToken { get; set; }
    public required string AccessToken { get; set; }
}
