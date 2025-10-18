using System.Diagnostics;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using Innts.Model;
using Innts.Model.Dto;
using Innts.Repository;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;

namespace Innts.Controllers;

/// <summary>
///     Класс управления аккаунтами пользователя.
/// </summary>
[Route("api/[controller]")]
[ApiController]
public class AccountController : ControllerBase
{
    private readonly IConfiguration _config;
    private readonly IBaseUserRepository<CustomUserTokenStorageModel> _dbUserRepository;
    private readonly ILogger<AccountController> _logger;
    private readonly SignInManager<CustomUser> _signInManager;
    private readonly UserManager<CustomUser> _userManager;
    public AccountController(ILogger<AccountController> logger,
        SignInManager<CustomUser> signInManager,
        UserManager<CustomUser> userManager,
        IConfiguration config,
        IBaseUserRepository<CustomUserTokenStorageModel> dbUserRepository)
    {
        _dbUserRepository = dbUserRepository;
        _logger = logger;
        _signInManager = signInManager;
        _userManager = userManager;
        _config = config;
    }

    [HttpPost]
    [Route("[action]/{id:int}")]
    [Authorize(Roles = "Admin")]
    public async Task<ActionResult> CreateAccount([FromBody] SignUpDto account)
    {
        var user = new CustomUser
        {
            UserName = account.Username,
            Email = account.Email,
            FirstName = account?.FirstName ?? "John",
            LastName = account?.LastName ?? "Doe",
            IsActivate = true
        };
        var result = _userManager.CreateAsync(user, "TestPassword1111!").Result;
        if (result.Succeeded) await _userManager.AddToRolesAsync(user, account?.Roles ?? ["Manager"]);
        return Ok(user);
    }
    /// <summary>
    ///     Функция авторизации пользователя.
    /// </summary>

    /// <param name="model">DTO Login user model</param>
    /// <returns>JWT token for user Auth</returns>
    [HttpPost]
    [ProducesResponseType(200)]
    [Route("Login")]
    public async Task<IActionResult> Login([FromBody] LoginDto model)
    {
        if (!ModelState.IsValid) return BadRequest();
        var user = await _userManager.FindByEmailAsync(model.Email);
        if (user == null) return Unauthorized();
        if (!user.IsActivate)
            return Unauthorized("Account has not activate! Ask System Administrator to activate your account!");
        var passwordCheck = await _signInManager.CheckPasswordSignInAsync(user, model.Password, false);
        if (!passwordCheck.Succeeded) return BadRequest();
        var roles = await _userManager.GetRolesAsync(user);
        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, user.Email??""),
            new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new(JwtRegisteredClaimNames.UniqueName, user.UserName??"")
        };
        var claimsIdentity = new ClaimsIdentity(claims, "Token");
        foreach (var claim in roles.Select(role => new Claim(ClaimTypes.Role, role)))
            claimsIdentity.AddClaim(claim);
        var token = GenerateToken(claimsIdentity.Claims);
        var refreshToken = GenerateRefreshToken();
        _dbUserRepository.AddNewUserRefreshToken(user.UserName ?? "", refreshToken);
        return Ok(new
        {
            accessToken = new JwtSecurityTokenHandler().WriteToken(token),
            refreshToken,
            expiration = token.ValidTo,
            user = new AuthUserDto
            {
                Email = model.Email,
                Roles = roles,
                Username = model.Email,
                IsActivate = user.IsActivate
            }
        });
    }
    /// <summary>
    ///     Обновление истёкшего токена с использованием RefreshToken
    /// </summary>
    /// <param name="model">Пара RefreshToken и AccessToken </param>
    /// <returns>Возвращает новую пару AccessToken, RefreshToken</returns>
    [HttpPost]
    [Route("Refresh")]
    public async Task<ActionResult<RefreshTokenDto>> Refresh([FromBody] RefreshTokenDto model)

    {
        var principal = GetPrincipalFromExpiredToken(model.AccessToken);
        if (principal == null) return BadRequest("Principals corrupted");
        var username = principal?.Identity?.Name;
        var savedRefreshToken =
            _dbUserRepository.GetRefreshTokenByUsername(username ?? ""); //retrieve the refresh token from a data store
        if (savedRefreshToken != model.RefreshToken) return BadRequest("Invalid refresh token");
        var newJwtToken = GenerateToken(principal?.Claims ?? []);
        var newRefreshToken = GenerateRefreshToken();
        _dbUserRepository.DeleteRefreshToken(username ?? "", model.RefreshToken);
        _dbUserRepository.SaveRefreshToken(username ?? "", newRefreshToken);
        var user = _userManager.Users.FirstOrDefault(c => c.UserName == username);
        if (user == null) return BadRequest("User not found");
        var roles = await _userManager.GetRolesAsync(user).ConfigureAwait(false);
        return Ok(new
        {
            accessToken = new JwtSecurityTokenHandler().WriteToken(newJwtToken),
            refreshToken = newRefreshToken,
            user = new AuthUserDto
            {
                Email = user.Email ?? "",
                Roles = roles,
                Username = user.Email ?? "",
                IsActivate = user.IsActivate
            }
        });
    }
    [HttpGet("CheckAuth")]
    [Authorize(Roles = "Admin, Medic, ContentManager, Expert")]
    public ActionResult CheckAuth()
    {
        return Ok();
    }
    /// <summary>
    ///     Функция выхода из системы.
    /// </summary>
    /// <returns>Статус 200 и удаляет последний RefreshToken из системы</returns>
    [HttpPost("Logout")]
    [Authorize(Roles = "Admin, Medic, ContentManager, Expert")]
    public ActionResult Logout()
    {
        var user = User.Identity?.Name;
        if (user == null) return BadRequest();
        try
        {
            var refreshToken = _dbUserRepository.GetRefreshTokenByUsername(user);
            _dbUserRepository.DeleteRefreshToken(user, refreshToken);
        }
        catch (Exception ex)
        {
            Debug.WriteLine(ex.Message);
        }
        return Ok();
    }

    /// <summary>
    ///     Генерирует токен.
    /// </summary>
    /// <param name="claims">Список атрибутов для генерации токена.</param>
    /// <remarks>Недоступен из внешнего API</remarks>
    /// <returns>Возвращает токен для дальнейшей авторизации</returns>
    [NonAction]
    private JwtSecurityToken GenerateToken(IEnumerable<Claim> claims)
    {
        var token = _config["Tokens:Key"];
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(token ?? "asdasdaksndjansdnk32k4"));
        var jwt = new JwtSecurityToken(
            _config["Tokens:Issuer"],
            _config["Tokens:Audience"],
            claims, //the user's claims, for example new Claim[] { new Claim(ClaimTypes.Name, "The username"), //... 

            DateTime.UtcNow,
            DateTime.UtcNow.AddDays(120),
            new SigningCredentials(key, SecurityAlgorithms.HmacSha256)
        );
        return jwt; //the method is called WriteToken but returns a string
    }

    /// <summary>
    ///     Генерирует новый RefreshToken.
    /// </summary>
    /// <returns>Возвращает новый RefreshToken </returns>
    /// <remarks>Не используется во внешнем API</remarks>
    [NonAction]
    private static string GenerateRefreshToken()
    {
        var randomNumber = new byte[32];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomNumber);
        return Convert.ToBase64String(randomNumber);
    }

    /// <summary>
    ///     Получает данные claims из протухшего токена.
    /// </summary>
    /// <param name="token"></param>
    /// <returns></returns>
    /// <exception cref="SecurityTokenException"></exception>
    /// <remarks>Не используется во внешнем API</remarks>
    [NonAction]
    private ClaimsPrincipal GetPrincipalFromExpiredToken(string token)
    {
        var tokenValidationParameters = new TokenValidationParameters
        {
            ValidateAudience =
                false, //you might want to validate the audience and issuer depending on your use case
            ValidateIssuer = false,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Tokens:Key"] ?? "asdasdaksndjansdnk32k4")),
            ValidateLifetime = false //here we are saying that we don't care about the token's expiration date
        };
        var tokenHandler = new JwtSecurityTokenHandler();
        var principal = tokenHandler.ValidateToken(token, tokenValidationParameters, out var securityToken);
        if (securityToken is not JwtSecurityToken jwtSecurityToken || !jwtSecurityToken.Header.Alg.Equals(
                SecurityAlgorithms.HmacSha256,
                StringComparison.InvariantCultureIgnoreCase))
            throw new SecurityTokenException("Invalid token");

        return principal;
    }
}

