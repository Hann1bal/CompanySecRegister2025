namespace Innts.Model.Files;
public class FileOperationResult
{
    public bool Success { get; set; }
    public string Message { get; set; }
    public string FilePath { get; set; }
    public byte[] FileContent { get; set; }
}

public class ImportResult<T>
{
    public bool Success { get; set; }
    public string Message { get; set; }
    public List<T> Data { get; set; } = new List<T>();
    public List<string> Errors { get; set; } = new List<string>();
}
