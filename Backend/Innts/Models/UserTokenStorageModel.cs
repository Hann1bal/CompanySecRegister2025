using System.ComponentModel.DataAnnotations;
namespace Innts.Model;

public class CustomUserTokenStorageModel
{
    [Key] public long TokenId { get; set; }
    public long UserId { get; set; }
    public required CustomUser User { get; set; }
    public required string RefreshToken { get; set; }
}