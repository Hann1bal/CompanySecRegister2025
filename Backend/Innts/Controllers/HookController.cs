
using System.Collections;
using System.Collections.Concurrent;
using System.Reflection;
using Innts.Controllers.Utils;
using Innts.Model;
using Innts.Model.Dto;
using Innts.Models;
using Innts.Repository;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace Innts.Controllers;

[ApiController]
[Route("api/[controller]")]
public class HookController(UserManager<CustomUser> userManager, IBaseRepository<CompanyModel> dbRepository) : ControllerBase
{

    private readonly UserManager<CustomUser> _userManager = userManager;
    private readonly IBaseRepository<CompanyModel> _dbRepository = dbRepository;

    [HttpPost]
    [Route("AddCompany1")]
    public async Task<ActionResult> AddCompany([FromBody] CompanyModelDto companyModelDto)
    {
        var data = EntityMapper.MapToEntity<CompanyModel, CompanyModelDto>(companyModelDto, new CompanyModel());
        await _dbRepository.Add(data);
        return Ok();
    }
    [HttpPost]
    [Route("AddBatch1")]
    public async Task<ActionResult> AddBatch([FromBody] List<CompanyModelDto> companyModelDto)
    {
        List<CompanyModel> companyModels = [];
        foreach (var company in companyModelDto)
            companyModels.Add(EntityMapper.MapToEntity<CompanyModel, CompanyModelDto>(company, new CompanyModel()));
        _dbRepository.AddList(companyModels);
        return Ok();
    }

}
