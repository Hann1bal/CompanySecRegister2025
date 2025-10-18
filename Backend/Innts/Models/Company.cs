namespace Innts.Models;

public class CompanyModel : IBaseModel
{
    public long Id { get; set; }
    public string inn { get; set; }
    public string orgName { get; set; } = String.Empty;
    public string orgFullName { get; set; } = String.Empty;
    public string status { get; set; } = String.Empty;
    public string legalAddress { get; set; } = String.Empty;
    public string productionAddress { get; set; } = String.Empty;
    public string director { get; set; } = string.Empty;
    public string okved_description { get; set; } = string.Empty;
    public string additionalSiteAddress { get; set; } = String.Empty;
    public string industry { get; set; } = String.Empty;
    public string subIndustry { get; set; } = String.Empty;
    public string mainOkved { get; set; } = String.Empty;
    public string mainOkvedActivity { get; set; } = String.Empty;
    public string productionOkved { get; set; } = String.Empty;
    public string registrationDate { get; set; } = String.Empty;
    public string head { get; set; } = String.Empty;
    public string parentOrgName { get; set; } = String.Empty;
    public int parentOrgInn { get; set; }
    public string managementContacts { get; set; } = String.Empty;
    public string orgContact { get; set; } = String.Empty;
    public string emergencyContact { get; set; } = String.Empty;
    public string website { get; set; } = String.Empty;
    public string email { get; set; } = String.Empty;
    public string supportMeasures { get; set; } = String.Empty;
    public string specialStatus { get; set; } = String.Empty;
    public string smeStatus { get; set; } = String.Empty;
    public int revenue2022 { get; set; }
    public int revenue2023 { get; set; }
    public int revenue2024 { get; set; }
    public int profit2022 { get; set; }
    public int profit2023 { get; set; }
    public int profit2024 { get; set; }
    public int staffTotal2022 { get; set; }
    public int staffTotal2023 { get; set; }
    public int staffTotal2024 { get; set; }
    public int staffMoscow2022 { get; set; }
    public int staffMoscow2023 { get; set; }
    public int staffMoscow2024 { get; set; }
    public int payrollTotal2022 { get; set; }
    public int payrollTotal2023 { get; set; }
    public int payrollTotal2024 { get; set; }
    public int payrollMoscow2022 { get; set; }
    public int payrollMoscow2023 { get; set; }
    public int payrollMoscow2024 { get; set; }
    public int avgSalaryTotal2022 { get; set; }
    public int avgSalaryTotal2023 { get; set; }
    public int avgSalaryTotal2024 { get; set; }
    public int avgSalaryMoscow2022 { get; set; }
    public int avgSalaryMoscow2023 { get; set; }
    public int avgSalaryMoscow2024 { get; set; }
    public int taxTotal2022 { get; set; }
    public int taxTotal2023 { get; set; }
    public int taxTotal2024 { get; set; }
    public int taxProfit2022 { get; set; }
    public int taxProfit2023 { get; set; }
    public int taxProfit2024 { get; set; }
    public int taxProperty2022 { get; set; }
    public int taxProperty2023 { get; set; }
    public int taxProperty2024 { get; set; }
    public int taxLand2022 { get; set; }
    public int taxLand2023 { get; set; }
    public int taxLand2024 { get; set; }
    public int taxNdfl2022 { get; set; }
    public int taxNdfl2023 { get; set; }
    public int taxNdfl2024 { get; set; }
    public int taxTransport2022 { get; set; }
    public int taxTransport2023 { get; set; }
    public int taxTransport2024 { get; set; }
    public int taxOther2022 { get; set; }
    public int taxOther2023 { get; set; }
    public int taxOther2024 { get; set; }
    public int excise2022 { get; set; }
    public int excise2023 { get; set; }
    public int excise2024 { get; set; }
    public int investMoscow2022 { get; set; }
    public int investMoscow2023 { get; set; }
    public int investMoscow2024 { get; set; }
    public int export2022 { get; set; }
    public int export2023 { get; set; }
    public int export2024 { get; set; }
    public string landCadastral { get; set; } = String.Empty;
    public int landArea { get; set; }
    public string landUse { get; set; } = String.Empty;
    public string landOwnership { get; set; } = String.Empty;
    public string landOwner { get; set; } = String.Empty;
    public string oksCadastral { get; set; } = String.Empty;
    public int oksArea { get; set; }
    public string oksUse { get; set; } = String.Empty;
    public string oksType { get; set; } = String.Empty;
    public string oksOwnership { get; set; } = String.Empty;
    public string oksOwner { get; set; } = String.Empty;
    public int productionArea { get; set; }
    public string standardizedProduct { get; set; } = String.Empty;
    public string productNames { get; set; } = String.Empty;
    public string productOkpd2 { get; set; } = String.Empty;
    public string productSegments { get; set; } = String.Empty;
    public string productCatalog { get; set; } = String.Empty;
    public string hasGovOrder { get; set; } = String.Empty;
    public string capacityUtilization { get; set; } = String.Empty;
    public string hasExport { get; set; } = String.Empty;
    public int exportPrevYear { get; set; }
    public string exportCountries { get; set; } = String.Empty;
    public string legalCoords { get; set; } = String.Empty;
    public string productionCoords { get; set; } = String.Empty;
    public string additionalCoords { get; set; } = String.Empty;
    public int latitude { get; set; }
    public int longitude { get; set; }
    public string okrug { get; set; } = String.Empty;
    public string district { get; set; } = String.Empty;
    public DateTime update_at = DateTime.Now;
    public DateTime create_at = DateTime.Now;
}