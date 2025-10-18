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
    
    // Группируем компании по основному ОКВЭД
    var groupedByOkved = data?
        .Where(c => !string.IsNullOrEmpty(c.mainOkved))
        .GroupBy(c => c.mainOkved)
        .ToDictionary(g => g.Key, g => g.ToList()) ?? new Dictionary<string, List<CompanyModel>>();

    foreach (var okvedGroup in groupedByOkved)
    {
        var companiesList = new List<CompaniesNode>();
        
        foreach (var company in okvedGroup.Value)
        {
            var staffList = new List<Staff>();
            
            // Добавляем директора, если информация есть
            if (!string.IsNullOrEmpty(company.head))
            {
                staffList.Add(new Staff 
                {
                    Id = company.head,
                    Name = company.head,
                    Role = "Директор" // Можно извлечь роль из строки, если нужно
                });
            }

            companiesList.Add(new CompaniesNode
            {
                Id = company.inn.ToString(), // Приводим к string, т.к. в JSON это строка
                Name = company.orgFullName,
                staff = staffList
            });
        }

        nodes.Add(new Node
        {
            Id = okvedGroup.Key,
            Name = okvedGroup.Value.First().mainOkvedActivity ?? "Не указано",
            URI = "", // Можно заполнить, если есть URL для ОКВЭД
            Companies = companiesList
        });
    }
}
    public void InitLinks()
    {

    }
}