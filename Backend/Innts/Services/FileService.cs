using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;
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
            using (SpreadsheetDocument spreadsheetDocument = SpreadsheetDocument.Open(fileStream, false))
            {
                WorkbookPart workbookPart = spreadsheetDocument.WorkbookPart;
                WorksheetPart worksheetPart = workbookPart.WorksheetParts.First();
                SheetData sheetData = worksheetPart.Worksheet.Elements<SheetData>().First();

                // Получаем SharedStringTable для чтения текстовых значений
                SharedStringTable sharedStringTable = workbookPart.SharedStringTablePart?.SharedStringTable;

                var rows = sheetData.Elements<Row>().Skip(1); // Пропускаем заголовок

                foreach (Row row in rows)
                {
                    try
                    {
                        var cells = row.Elements<Cell>().ToArray();

                        var company = new CompanyModel
                        {
                            inn = GetCellValue(cells.Length > 0 ? cells[1] : null, sharedStringTable),
                            orgName = GetCellValue(cells.Length > 1 ? cells[1] : null, sharedStringTable) ?? "",
                            orgFullName = GetCellValue(cells.Length > 2 ? cells[2] : null, sharedStringTable) ?? "",
                            status = GetCellValue(cells.Length > 3 ? cells[3] : null, sharedStringTable) ?? "",
                            legalAddress = GetCellValue(cells.Length > 4 ? cells[4] : null, sharedStringTable) ?? "",
                            mainOkved = GetCellValue(cells.Length > 5 ? cells[5] : null, sharedStringTable) ?? "",
                            head = GetCellValue(cells.Length > 6 ? cells[6] : null, sharedStringTable) ?? "",
                            email = GetCellValue(cells.Length > 7 ? cells[7] : null, sharedStringTable) ?? "",
                            website = GetCellValue(cells.Length > 8 ? cells[8] : null, sharedStringTable) ?? ""
                        };

                        // Проверяем, что ИНН не пустой (базовая валидация)
                        if (!string.IsNullOrEmpty(company.inn))
                        {
                            result.Data.Add(company);
                        }
                    }
                    catch (Exception ex)
                    {
                        result.Errors.Add($"Ошибка в строке {row.RowIndex}: {ex.Message}");
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

    // Вспомогательный метод для получения значения ячейки
    private string GetCellValue(Cell cell, SharedStringTable sharedStringTable)
    {
        if (cell == null || cell.CellValue == null)
            return string.Empty;

        string cellValue = cell.CellValue.Text;

        if (cell.DataType != null && cell.DataType.Value == CellValues.SharedString)
        {
            // Если это shared string, получаем значение из таблицы
            if (int.TryParse(cellValue, out int index) && sharedStringTable != null)
            {
                if (index >= 0 && index < sharedStringTable.Elements<SharedStringItem>().Count())
                {
                    return sharedStringTable.ElementAt(index).InnerText;
                }
            }
        }

        return cellValue;
    }

    public Task<ImportResult<CompanyModel>> ImportCompaniesFromPdf(Stream fileStream)
    {
        throw new NotImplementedException();
    }
}