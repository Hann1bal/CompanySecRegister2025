export interface ICompany {
  // Обязательные поля
  inn: string;
  orgName: string;
  orgFullName: string;
  status: string;
  legalAddress: string;

  // Остальные — необязательные
  productionAddress?: string;
  additionalSiteAddress?: string;
  industry?: string;
  subIndustry?: string;
  mainOkved?: string;
  mainOkvedActivity?: string;
  productionOkved?: string;
  registrationDate?: string;
  head?: string;
  parentOrgName?: string;
  parentOrgInn?: number;
  managementContacts?: string;
  orgContact?: string;
  emergencyContact?: string;
  website?: string;
  email?: string;
  supportMeasures?: string;
  specialStatus?: string;
  smeStatus?: string;

  // Финансовые показатели
  revenue2022?: number;
  revenue2023?: number;
  revenue2024?: number;
  profit2022?: number;
  profit2023?: number;
  profit2024?: number;

  // Персонал
  staffTotal2022?: number;
  staffTotal2023?: number;
  staffTotal2024?: number;
  staffMoscow2022?: number;
  staffMoscow2023?: number;
  staffMoscow2024?: number;

  // ФОТ
  payrollTotal2022?: number;
  payrollTotal2023?: number;
  payrollTotal2024?: number;
  payrollMoscow2022?: number;
  payrollMoscow2023?: number;
  payrollMoscow2024?: number;

  // Средняя зарплата
  avgSalaryTotal2022?: number;
  avgSalaryTotal2023?: number;
  avgSalaryTotal2024?: number;
  avgSalaryMoscow2022?: number;
  avgSalaryMoscow2023?: number;
  avgSalaryMoscow2024?: number;

  // Налоги
  taxTotal2022?: number;
  taxTotal2023?: number;
  taxTotal2024?: number;
  taxProfit2022?: number;
  taxProfit2023?: number;
  taxProfit2024?: number;
  taxProperty2022?: number;
  taxProperty2023?: number;
  taxProperty2024?: number;
  taxLand2022?: number;
  taxLand2023?: number;
  taxLand2024?: number;
  taxNdfl2022?: number;
  taxNdfl2023?: number;
  taxNdfl2024?: number;
  taxTransport2022?: number;
  taxTransport2023?: number;
  taxTransport2024?: number;
  taxOther2022?: number;
  taxOther2023?: number;
  taxOther2024?: number;

  // Акцизы и инвестиции
  excise2022?: number;
  excise2023?: number;
  excise2024?: number;
  investMoscow2022?: number;
  investMoscow2023?: number;
  investMoscow2024?: number;

  // Экспорт
  export2022?: number;
  export2023?: number;
  export2024?: number;
  hasExport?: string;
  exportPrevYear?: number;
  exportCountries?: string;

  // Земля
  landCadastral?: string;
  landArea?: number;
  landUse?: string;
  landOwnership?: string;
  landOwner?: string;

  // ОКС (строения)
  oksCadastral?: string;
  oksArea?: number;
  oksUse?: string;
  oksType?: string;
  oksOwnership?: string;
  oksOwner?: string;

  // Производственные данные
  productionArea?: number;
  standardizedProduct?: string;
  productNames?: string;
  productOkpd2?: string;
  productSegments?: string;
  productCatalog?: string;
  hasGovOrder?: string;
  capacityUtilization?: string;

  // Координаты
  legalCoords?: string;
  productionCoords?: string;
  additionalCoords?: string;
  latitude?: number;
  longitude?: number;

  // География
  okrug?: string;
  district?: string;
}
