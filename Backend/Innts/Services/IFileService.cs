using Innts.Model.Files;
using Innts.Models;
namespace Innts.Services;

public interface IFileService
{
    Task<FileOperationResult> ExportCompaniesToPdf(List<CompanyModel> companies);
    Task<FileOperationResult> ExportCompaniesToExcel(List<CompanyModel> companies);
    Task<ImportResult<CompanyModel>> ImportCompaniesFromPdf(Stream fileStream);
    Task<ImportResult<CompanyModel>> ImportCompaniesFromExcel(Stream fileStream);
}

