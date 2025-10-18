using System.Diagnostics.CodeAnalysis;

namespace Innts.Model.Dto
{
    public class CompanyModelDto
    {
        public string inn { get; set; }
        public string orgName { get; set; } = string.Empty;
        public string orgFullName { get; set; } = string.Empty;
        public string status { get; set; } = string.Empty;
        public string legalAddress { get; set; } = string.Empty;

         public string? productionAddress { get; set; }
         public string? additionalSiteAddress { get; set; }
         public string? industry { get; set; }
         public string? subIndustry { get; set; }
         public string? mainOkved { get; set; }
         public string? mainOkvedActivity { get; set; }
         public string? productionOkved { get; set; }
         public string? registrationDate { get; set; }
         public string? head { get; set; }
         public string? parentOrgName { get; set; }
         public int? parentOrgInn { get; set; }
         public string? managementContacts { get; set; }
         public string? orgContact { get; set; }
         public string? emergencyContact { get; set; }
         public string? website { get; set; }
         public string? email { get; set; }
         public string? supportMeasures { get; set; }
         public string? specialStatus { get; set; }
         public string? smeStatus { get; set; }

         public int? revenue2022 { get; set; }
         public int? revenue2023 { get; set; }
         public int? revenue2024 { get; set; }
         public int? profit2022 { get; set; }
         public int? profit2023 { get; set; }
         public int? profit2024 { get; set; }
         public int? staffTotal2022 { get; set; }
         public int? staffTotal2023 { get; set; }
         public int? staffTotal2024 { get; set; }
         public int? staffMoscow2022 { get; set; }
         public int? staffMoscow2023 { get; set; }
         public int? staffMoscow2024 { get; set; }
         public int? payrollTotal2022 { get; set; }
         public int? payrollTotal2023 { get; set; }
         public int? payrollTotal2024 { get; set; }
         public int? payrollMoscow2022 { get; set; }
         public int? payrollMoscow2023 { get; set; }
         public int? payrollMoscow2024 { get; set; }
         public int? avgSalaryTotal2022 { get; set; }
         public int? avgSalaryTotal2023 { get; set; }
         public int? avgSalaryTotal2024 { get; set; }
         public int? avgSalaryMoscow2022 { get; set; }
         public int? avgSalaryMoscow2023 { get; set; }
         public int? avgSalaryMoscow2024 { get; set; }

         public int? taxTotal2022 { get; set; }
         public int? taxTotal2023 { get; set; }
         public int? taxTotal2024 { get; set; }
         public int? taxProfit2022 { get; set; }
         public int? taxProfit2023 { get; set; }
         public int? taxProfit2024 { get; set; }
         public int? taxProperty2022 { get; set; }
         public int? taxProperty2023 { get; set; }
         public int? taxProperty2024 { get; set; }
         public int? taxLand2022 { get; set; }
         public int? taxLand2023 { get; set; }
         public int? taxLand2024 { get; set; }
         public int? taxNdfl2022 { get; set; }
         public int? taxNdfl2023 { get; set; }
         public int? taxNdfl2024 { get; set; }
         public int? taxTransport2022 { get; set; }
         public int? taxTransport2023 { get; set; }
         public int? taxTransport2024 { get; set; }
         public int? taxOther2022 { get; set; }
         public int? taxOther2023 { get; set; }
         public int? taxOther2024 { get; set; }

         public int? excise2022 { get; set; }
         public int? excise2023 { get; set; }
         public int? excise2024 { get; set; }
         public int? investMoscow2022 { get; set; }
         public int? investMoscow2023 { get; set; }
         public int? investMoscow2024 { get; set; }
         public int? export2022 { get; set; }
         public int? export2023 { get; set; }
         public int? export2024 { get; set; }

         public string? landCadastral { get; set; }
         public int? landArea { get; set; }
         public string? landUse { get; set; }
         public string? landOwnership { get; set; }
         public string? landOwner { get; set; }

         public string? oksCadastral { get; set; }
         public int? oksArea { get; set; }
         public string? oksUse { get; set; }
         public string? oksType { get; set; }
         public string? oksOwnership { get; set; }
         public string? oksOwner { get; set; }

         public int? productionArea { get; set; }
         public string? standardizedProduct { get; set; }
         public string? productNames { get; set; }
         public string? productOkpd2 { get; set; }
         public string? productSegments { get; set; }
         public string? productCatalog { get; set; }
         public string? hasGovOrder { get; set; }
         public string? capacityUtilization { get; set; }
         public string? hasExport { get; set; }
         public int? exportPrevYear { get; set; }
         public string? exportCountries { get; set; }
         public string? legalCoords { get; set; }
         public string? productionCoords { get; set; }
         public string? additionalCoords { get; set; }
         public int? latitude { get; set; }
         public int? longitude { get; set; }
         public string? okrug { get; set; }
         public string? district { get; set; }
    }
}
