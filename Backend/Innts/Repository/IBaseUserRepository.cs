namespace Innts.Repository;

public interface IBaseUserRepository<T> where T : class
{
    string GetRefreshTokenByUsername(string username);
    void DeleteRefreshToken(string username, string refreshToken);
    void SaveRefreshToken(string username, string newRefreshToken);
    void AddNewUserRefreshToken(string username, string newRefreshToken);

}