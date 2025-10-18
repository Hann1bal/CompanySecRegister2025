
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
public class DataController(UserManager<CustomUser> userManager, IBaseRepository<CompanyModel> dbRepository) : ControllerBase
{

    private readonly UserManager<CustomUser> _userManager = userManager;
    private readonly IBaseRepository<CompanyModel> _dbRepository = dbRepository;

    [HttpPut]
    public async Task<ActionResult> UpdateCompany()
    {
        return Ok();
    }

    [HttpPost]
    public async Task<ActionResult> AddCompany([FromBody] CompanyModelDto companyModelDto)
    {
        var data = EntityMapper.MapToEntity<CompanyModel, CompanyModelDto>(companyModelDto, new CompanyModel());
        await _dbRepository.Add(data);
        return Ok(data);
    }
    [HttpGet]
    public async Task<ActionResult> GetAll()
    {
        var data = _dbRepository.GetAll();
        return Ok(data);
    }
    [HttpPost]
    public async Task<ActionResult> UploadFile(List<IFormFile> files)
    {
        long size = files.Sum(f => f.Length);

        foreach (var formFile in files)
        {
            if (formFile.Length > 0)
            {
                var filePath = Path.GetTempFileName();
                using var stream = System.IO.File.Create(filePath);
                await formFile.CopyToAsync(stream);
            }
        }

        // Process uploaded files
        // Don't rely on or trust the FileName property without validation.

        return Ok(new { count = files.Count, size });
    }

    [HttpGet]
    public async Task<ActionResult> GetData([FromBody] CompanyFinderDto model)
    {
        if (model.INN is not null)
            return Ok(await _dbRepository.FindById(model.INN ?? 0, ""));
        else if (model.CompanyName is not null)
            return Ok(await _dbRepository.FindByIdAsync(0, model.CompanyName));
        else
            return BadRequest("WrongRequest");
    }

}