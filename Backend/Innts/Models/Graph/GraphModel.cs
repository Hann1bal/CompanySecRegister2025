public class Graph
{
    public long Id { get; set; }
    public string? Name { get; set; }
    public long RootId { get; set; }
    public List<Node> Nodes { get; set; }
    public List<Links> Links { get; set; }
}