using Innts.Model.Files;
using Innts.Models;
namespace Innts.Services;

public class FileService : IFileService
{
    private readonly IWebHostEnvironment _environment;
    private readonly string _filesDirectory;

    public FileService(IWebHostEnvironment environment)
    {
        _environment = environment;
        _filesDirectory = Path.Combine(_environment.ContentRootPath, "Files");

        if (!Directory.Exists(_filesDirectory))
            Directory.CreateDirectory(_filesDirectory);
    }

    // Экспорт в PDF
    public async Task<FileOperationResult> ExportCompaniesToPdf(List<CompanyModel> companies)
    {
        try
        {
            using (var memoryStream = new MemoryStream())
            {
                var document = new iTextSharp.text.Document();
                var writer = iTextSharp.text.pdf.PdfWriter.GetInstance(document, memoryStream);

                document.Open();

                // Заголовок
                var title = new iTextSharp.text.Paragraph("Список компаний")
                {
                    Alignment = iTextSharp.text.Element.ALIGN_CENTER,
                    SpacingAfter = 20f
                };
                document.Add(title);

                // Таблица с данными
                var table = new iTextSharp.text.pdf.PdfPTable(4);
                table.WidthPercentage = 100;

                // Заголовки таблицы
                table.AddCell("ИНН");
                table.AddCell("Название");
                table.AddCell("Статус");
                table.AddCell("Директор");

                // Данные компаний
                foreach (var company in companies)
                {
                    table.AddCell(company.inn.ToString());
                    table.AddCell(company.orgName);
                    table.AddCell(company.status);
                    table.AddCell(company.head);
                }

                document.Add(table);
                document.Close();

                var fileName = $"companies_{DateTime.Now:yyyyMMddHHmmss}.pdf";
                var filePath = Path.Combine(_filesDirectory, fileName);

                await File.WriteAllBytesAsync(filePath, memoryStream.ToArray());

                return new FileOperationResult
                {
                    Success = true,
                    Message = "PDF файл успешно создан",
                    FilePath = filePath,
                    FileContent = memoryStream.ToArray()
                };
            }
        }
        catch (Exception ex)
        {
            return new FileOperationResult
            {
                Success = false,
                Message = $"Ошибка при создании PDF: {ex.Message}"
            };
        }
    }

    // Экспорт в Excel
    public async Task<FileOperationResult> ExportCompaniesToExcel(List<CompanyModel> companies)
    {
        try
        {
            using (var package = new OfficeOpenXml.ExcelPackage())
            {
                var worksheet = package.Workbook.Worksheets.Add("Компании");

                // Заголовки
                worksheet.Cells[1, 1].Value = "ИНН";
                worksheet.Cells[1, 2].Value = "Название";
                worksheet.Cells[1, 3].Value = "Полное название";
                worksheet.Cells[1, 4].Value = "Статус";
                worksheet.Cells[1, 5].Value = "Адрес";
                worksheet.Cells[1, 6].Value = "Основной ОКВЭД";
                worksheet.Cells[1, 7].Value = "Директор";
                worksheet.Cells[1, 8].Value = "Email";
                worksheet.Cells[1, 9].Value = "Сайт";

                // Стиль для заголовков
                using (var range = worksheet.Cells[1, 1, 1, 9])
                {
                    range.Style.Font.Bold = true;
                    range.Style.Fill.PatternType = OfficeOpenXml.Style.ExcelFillStyle.Solid;
                    range.Style.Fill.BackgroundColor.SetColor(System.Drawing.Color.LightGray);
                }

                // Данные
                for (int i = 0; i < companies.Count; i++)
                {
                    var company = companies[i];
                    var row = i + 2;

                    worksheet.Cells[row, 1].Value = company.inn;
                    worksheet.Cells[row, 2].Value = company.orgName;
                    worksheet.Cells[row, 3].Value = company.orgFullName;
                    worksheet.Cells[row, 4].Value = company.status;
                    worksheet.Cells[row, 5].Value = company.legalAddress;
                    worksheet.Cells[row, 6].Value = company.mainOkved;
                    worksheet.Cells[row, 7].Value = company.head;
                    worksheet.Cells[row, 8].Value = company.email;
                    worksheet.Cells[row, 9].Value = company.website;
                }

                // Авто-ширина колонок
                worksheet.Cells[worksheet.Dimension.Address].AutoFitColumns();

                var fileName = $"companies_{DateTime.Now:yyyyMMddHHmmss}.xlsx";
                var filePath = Path.Combine(_filesDirectory, fileName);

                await package.SaveAsAsync(new FileInfo(filePath));

                return new FileOperationResult
                {
                    Success = true,
                    Message = "Excel файл успешно создан",
                    FilePath = filePath,
                    FileContent = package.GetAsByteArray()
                };
            }
        }
        catch (Exception ex)
        {
            return new FileOperationResult
            {
                Success = false,
                Message = $"Ошибка при создании Excel: {ex.Message}"
            };
        }
    }

    // Импорт из Excel
    public async Task<ImportResult<CompanyModel>> ImportCompaniesFromExcel(Stream fileStream)
    {
        var result = new ImportResult<CompanyModel>();

        try
        {
            using (var package = new OfficeOpenXml.ExcelPackage(fileStream))
            {
                var worksheet = package.Workbook.Worksheets[0];
                var rowCount = worksheet.Dimension.Rows;

                for (int row = 2; row <= rowCount; row++) // Пропускаем заголовок
                {
                    try
                    {
                        var company = new CompanyModel
                        {
                            inn = worksheet.Cells[row, 1].Value.ToString(),
                            orgName = worksheet.Cells[row, 2].Value?.ToString() ?? "",
                            orgFullName = worksheet.Cells[row, 3].Value?.ToString() ?? "",
                            status = worksheet.Cells[row, 4].Value?.ToString() ?? "",
                            legalAddress = worksheet.Cells[row, 5].Value?.ToString() ?? "",
                            mainOkved = worksheet.Cells[row, 6].Value?.ToString() ?? "",
                            head = worksheet.Cells[row, 7].Value?.ToString() ?? "",
                            email = worksheet.Cells[row, 8].Value?.ToString() ?? "",
                            website = worksheet.Cells[row, 9].Value?.ToString() ?? ""
                        };

                        result.Data.Add(company);
                    }
                    catch (Exception ex)
                    {
                        result.Errors.Add($"Ошибка в строке {row}: {ex.Message}");
                    }
                }

                result.Success = true;
                result.Message = $"Успешно импортировано {result.Data.Count} компаний";
            }
        }
        catch (Exception ex)
        {
            result.Success = false;
            result.Message = $"Ошибка при чтении Excel: {ex.Message}";
        }

        return result;
    }

    public Task<ImportResult<CompanyModel>> ImportCompaniesFromPdf(Stream fileStream)
    {
        throw new NotImplementedException();
    }
}