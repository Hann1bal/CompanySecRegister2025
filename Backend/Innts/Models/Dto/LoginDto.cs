using System.ComponentModel.DataAnnotations;
namespace Innts.Model.Dto;

public class LoginDto
{
    [Required]
    [DataType(DataType.EmailAddress)]
    public required string Email { get; set; }

    [Required] public required string Password { get; set; }
}
