namespace Innts.Repository;
public interface IBaseRepository<T> where T : class
{
    Task<bool> Add(T item);

    void AddList(List<T> item);

    List<T> GetAll();
    Task<T> FindById(string id, string ids);
    Task<T> FindByIdAsync(long id, string ids);
    void Update(T item);
    void UpdateList(List<T> item);

    void Remove(int id);
    void Restore(int id);

}