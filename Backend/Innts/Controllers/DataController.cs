
using System.Collections;
using System.Collections.Concurrent;
using System.Reflection;
using Innts.Model;
using Innts.Model.Dto;
using Innts.Models;
using Innts.Repository;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace Innts.Controllers;

[ApiController]
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

                using (var stream = System.IO.File.Create(filePath))
                {
                    await formFile.CopyToAsync(stream);
                }
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
[AttributeUsage(AttributeTargets.Property)]
public class IgnoreOnUpdateAttribute : Attribute { }

public static class EntityMapper
{
    public static TModel MapToEntity<TModel, TDto>(TDto dto, TModel entity)
        where TModel : class
    {
        var dtoProperties = typeof(TDto).GetProperties();

        foreach (var dtoProp in dtoProperties)
        {
            if (dtoProp.GetCustomAttribute<IgnoreOnUpdateAttribute>() != null)
                continue;

            var entityProp = typeof(TModel).GetProperty(dtoProp.Name);
            if (entityProp == null || !entityProp.CanWrite) continue;

            var value = dtoProp.GetValue(dto);
            if (!IsEmpty(value))
            {
                entityProp.SetValue(entity, value);
            }
        }

        return entity;
    }
    private static readonly ConcurrentDictionary<Type, object> _defaultValues = new();

    private static object GetDefaultValue(Type type)
    {
        return _defaultValues.GetOrAdd(type, t =>
            t.IsValueType ? Activator.CreateInstance(t) : null);
    }
    private static bool IsEmpty(object value)
    {
        return value switch
        {
            null => true,
            string s => string.IsNullOrWhiteSpace(s),
            ICollection c => c.Count == 0,
            IEnumerable e => !e.GetEnumerator().MoveNext(),
            _ => value.Equals(GetDefaultValue(value.GetType()))
        };
    }
}

