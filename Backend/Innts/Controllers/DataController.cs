
using System.Reflection;
using Innts.Context;
using Innts.Controllers.Utils;
using Innts.Model;
using Innts.Model.Dto;
using Innts.Models;
using Innts.Repository;
using Innts.Services;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Innts.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DataController(IBaseRepository<CompanyModel> dbRepository, IDbContextFactory<DatabaseContext> dbContext, IFileService fileService) : ControllerBase
{

    // private readonly UserManager<CustomUser> _userManager = userManager;
    private readonly IBaseRepository<CompanyModel> _dbRepository = dbRepository;
    private readonly IDbContextFactory<DatabaseContext> dbContext = dbContext;
    private readonly IFileService _fileService = fileService;

    [HttpPut]
    [Route("UpdateCompany/{inn}")]
    public async Task<ActionResult> UpdateCompany(string inn, [FromBody] Dictionary<string, object> updateFields)
    {
        var _context = await dbContext.CreateDbContextAsync();
        try
        {
            // Находим компанию по ИНН
            var company = await _context.Companies.FirstOrDefaultAsync(c => c.orgFullName == inn);

            if (company == null)
            {
                return NotFound($"Компания с ИНН {inn} не найдена");
            }

            // Получаем все свойства модели компании
            var properties = typeof(CompanyModel).GetProperties(BindingFlags.Public | BindingFlags.Instance);
            var updatedProperties = new List<string>();

            foreach (var field in updateFields)
            {
                var property = properties.FirstOrDefault(p =>
                    p.Name.Equals(field.Key, StringComparison.OrdinalIgnoreCase) &&
                    p.CanWrite);

                if (property == null)
                {
                    return BadRequest($"Свойство {field.Key} не найдено или недоступно для записи");
                }

                try
                {
                    // Преобразуем значение к правильному типу
                    object convertedValue = ConvertValue(field.Value, property.PropertyType);
                    property.SetValue(company, convertedValue);
                    updatedProperties.Add(field.Key);
                }
                catch (Exception ex)
                {
                    return BadRequest($"Ошибка при установке значения для свойства {field.Key}: {ex.Message}");
                }
            }

            // Обновляем временную метку
            company.update_at = DateTime.UtcNow;

            // Сохраняем изменения
            await _context.SaveChangesAsync();

            return Ok(new
            {
                message = "Компания успешно обновлена",
                inn = inn,
                updatedFields = updatedProperties
            });
        }
        catch (DbUpdateException ex)
        {
            return StatusCode(500, $"Ошибка базы данных: {ex.Message}");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Внутренняя ошибка сервера: {ex.Message}");
        }
    }
    [NonAction]
    // Вспомогательный метод для преобразования значений
    private object ConvertValue(object value, Type targetType)
    {
        if (value == null)
            return null;

        var sourceType = value.GetType();

        // Если типы совпадают, возвращаем как есть
        if (targetType.IsAssignableFrom(sourceType))
            return value;

        // Обработка nullables
        if (targetType.IsGenericType && targetType.GetGenericTypeDefinition() == typeof(Nullable<>))
        {
            if (string.IsNullOrEmpty(value.ToString()))
                return null;

            targetType = Nullable.GetUnderlyingType(targetType);
        }

        // Специальная обработка для разных типов
        try
        {
            // Для числовых типов
            if (targetType == typeof(int) || targetType == typeof(int?))
            {
                if (int.TryParse(value.ToString(), out int result))
                    return result;
            }
            else if (targetType == typeof(long) || targetType == typeof(long?))
            {
                if (long.TryParse(value.ToString(), out long result))
                    return result;
            }
            // Для дат
            else if (targetType == typeof(DateTime) || targetType == typeof(DateTime?))
            {
                if (DateTime.TryParse(value.ToString(), out DateTime result))
                    return result;
            }
            // Для булевых значений
            else if (targetType == typeof(bool) || targetType == typeof(bool?))
            {
                if (bool.TryParse(value.ToString(), out bool result))
                    return result;
            }
            // Для строк - просто ToString()
            else if (targetType == typeof(string))
            {
                return value.ToString();
            }

            // Стандартное преобразование
            return Convert.ChangeType(value, targetType);
        }
        catch
        {
            throw new InvalidCastException($"Не удалось преобразовать значение '{value}' к типу {targetType.Name}");
        }
    }
    // Импорт компаний из Excel
    [HttpPost]
    [Route("/ImportFromExcel")]
    public async Task<IActionResult> ImportFromExcel(IFormFile file)
    {
        var _context = await dbContext.CreateDbContextAsync();
        if (file == null || file.Length == 0)
            return BadRequest("Файл не выбран");

        if (!Path.GetExtension(file.FileName).Equals(".xlsx", StringComparison.OrdinalIgnoreCase))
            return BadRequest("Поддерживаются только файлы .xlsx");

        try
        {
            using (var stream = file.OpenReadStream())
            {
                var result = await _fileService.ImportCompaniesFromExcel(stream);

                if (!result.Success)
                    return BadRequest(result.Message);

                // Сохранение импортированных данных в БД
                foreach (var company in result.Data)
                {
                    var existing = await _context.Companies
                        .FirstOrDefaultAsync(c => c.inn == company.inn);

                    if (existing != null)
                    {
                        // Обновление существующей компании
                        _context.Entry(existing).CurrentValues.SetValues(company);
                    }
                    else
                    {
                        // Добавление новой компании
                        await _context.Companies.AddAsync(company);
                    }
                }

                await _context.SaveChangesAsync();

                return Ok(new
                {
                    message = result.Message,
                    importedCount = result.Data.Count,
                    errors = result.Errors
                });
            }
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Ошибка при импорте: {ex.Message}");
        }
    }
    [HttpPost]
    [Route("AddCompany")]
    public async Task<ActionResult> AddCompany([FromBody] CompanyModelDto companyModelDto)
    {
        var data = EntityMapper.MapToEntity<CompanyModel, CompanyModelDto>(companyModelDto, new CompanyModel());
        await _dbRepository.Add(data);
        return Ok(data);
    }
    [HttpGet]
    [Route("GetAll")]
    public async Task<ActionResult> GetAll()
    {
        var data = _dbRepository.GetAll();
        return Ok(data);
    }
    [HttpPost]
    [Route("UploadFile")]
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
    [Route("GetData")]
    public async Task<ActionResult> GetData([FromBody] CompanyFinderDto model)
    {
        if (model.INN is not null)
            return Ok(await _dbRepository.FindById(model.INN ?? "0", ""));
        else if (model.CompanyName is not null)
            return Ok(await _dbRepository.FindByIdAsync(0, model.CompanyName));
        else
            return BadRequest("WrongRequest");
    }

}