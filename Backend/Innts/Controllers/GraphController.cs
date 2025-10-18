using Innts.Controllers.Utils;
using Innts.Model.Dto;
using Innts.Models;
using Innts.Repository;
using Microsoft.AspNetCore.Mvc;

namespace Innts.Controllers;

[ApiController]
[Route("api/[controller]")]
public class GraphController(IBaseRepository<CompanyModel> dbRepository, TestService testService) : ControllerBase
{
    private readonly TestService _testService = testService;
    private readonly IBaseRepository<CompanyModel> _dbRepository = dbRepository;

    [HttpGet]
    public async Task<ActionResult> GetGraph()
    {
        _testService.InitNodes();
        _testService.InitLinks();
        _testService.InitGraph();

        var Graph = _testService.graph;
        return Ok(Graph);
    }
    [HttpPost]
    public async Task<ActionResult> AddBatch([FromBody] List<CompanyModelDto> companyModelDto)
    {
        List<CompanyModel> companyModels = [];
        foreach (var company in companyModelDto)
            companyModels.Add(EntityMapper.MapToEntity<CompanyModel, CompanyModelDto>(company, new CompanyModel()));
        _dbRepository.AddList(companyModels);
        return Ok();
    }

}
