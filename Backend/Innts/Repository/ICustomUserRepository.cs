using Innts.Context;
using Innts.Model;
using Microsoft.EntityFrameworkCore;

namespace Innts.Repository;

public class KbUserTokenStorageRepository : IBaseUserRepository<CustomUserTokenStorageModel>
{
    private readonly IDbContextFactory<DatabaseContext> _context;

    public KbUserTokenStorageRepository(IDbContextFactory<DatabaseContext> context)
    {
        _context = context;
    }

    public string GetRefreshTokenByUsername(string username)
    {
        using var db = _context.CreateDbContext();
        return db.TokenStorage.Any(x => x.User.UserName == username)
            ? db.TokenStorage.Where(l => l.User.UserName == username).ToList()[0].RefreshToken
            : "Not Found";
    }

    public void AddNewUserRefreshToken(string username, string refreshToken)
    {
        using var db = _context.CreateDbContext();

        var user = db.Users.First(c => c.UserName == username);
        if (!db.TokenStorage.Any(c => c.User.UserName == username))
        {
            var tokenUser = new CustomUserTokenStorageModel
            {
                User = user,
                RefreshToken = refreshToken,
                UserId = user.Id
            };
            db.TokenStorage.Add(tokenUser);
        }
        else
        {
            var existToken = db.TokenStorage.First(c => c.User.UserName == username);
            existToken.RefreshToken = refreshToken;
            db.TokenStorage.Update(existToken);
        }


        db.SaveChanges();
    }

    public void DeleteRefreshToken(string username, string refreshToken)
    {
        using var db = _context.CreateDbContext();

        var token = db.TokenStorage.First(c => c.User.UserName == username);
        db.TokenStorage.Remove(token);
        db.SaveChanges();
    }

    public void SaveRefreshToken(string username, string newRefreshToken)
    {
        using var db = _context.CreateDbContext();

        var user = db.Users.First(c => c.UserName == username);
        var tokenUser = new CustomUserTokenStorageModel
        {
            User = user,
            RefreshToken = newRefreshToken,
            UserId = user.Id
        };
        db.TokenStorage.Add(tokenUser);
        db.SaveChanges();
    }
}