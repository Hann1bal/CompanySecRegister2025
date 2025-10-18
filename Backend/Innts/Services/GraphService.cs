using Innts.Models;
using Newtonsoft.Json;

public class TestService(HttpClientService httpClientService)
{
    public List<Node> nodes = [];
    public List<Links> links = [];
    public Graph graph { get; set; } = new Graph { };
    public readonly HttpClientService _httpService = httpClientService;

    public void InitGraph()
    {
        graph = new Graph
        {
            Id = 0,
            Name = "test_graph",
            Nodes = nodes,
            Links = links
        };
    }
    public async Task InitNodes()
    {
        var result = await _httpService.GetAsync("{0}/api/v1/companies?page=1&size=50");
        var data = JsonConvert.DeserializeObject<List<CompanyModel>>(result);
        foreach (var company in data ?? [])
        {
            nodes.Add(new Node
            {
                Id = company.mainOkved,
                Name = company.productionOkved,
                Companies = new List<CompaniesNode>([new CompaniesNode{
                    Id = company.inn.ToString(),
                    Name = company.orgFullName,
                    staff = new List<Staff>([   new Staff {
                        Id = company.head,
                        Name = company.head,
                    }])

                }])
            });
        }
    }
    public void InitLinks()
    {

    }
}