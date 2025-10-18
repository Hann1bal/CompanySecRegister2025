import React, { useState, useMemo, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { Button, TextInput } from "flowbite-react";
import { FaEdit, FaSearch } from "react-icons/fa";
import { useStores } from "../context/root-store-context";
import { observer } from "mobx-react-lite";

const fieldDictionary: Record<string, string> = {
  inn: "ИНН",
  orgName: "Наименование организации",
  orgFullName: "Полное наименование организации",
  status: "Статус",
  legalAddress: "Юридический адрес",
  productionAddress: "Адрес производства",
  additionalSiteAddress: "Адрес дополнительной площадки",
  industry: "Основная отрасль",
  subIndustry: "Подотрасль (Основная)",
  mainOkved: "Основной ОКВЭД",
  mainOkvedActivity: "Вид деятельности по основному ОКВЭД",
  productionOkved: "Производственный ОКВЭД",
  registrationDate: "Дата регистрации",
  head: "Руководитель",
  parentOrgName: "Головная организация",
  parentOrgInn: "ИНН головной организации",
  managementContacts: "Контактные данные руководства",
  orgContact: "Контакт сотрудника организации",
  emergencyContact: "Контактные данные ответственного по ЧС",
  website: "Сайт",
  email: "Электронная почта",
  supportMeasures: "Меры поддержки",
  specialStatus: "Наличие особого статуса",
  smeStatus: "Статус МСП",

  // Финансы
  revenue2022: "Выручка, тыс. руб. (2022)",
  revenue2023: "Выручка, тыс. руб. (2023)",
  revenue2024: "Выручка, тыс. руб. (2024)",
  profit2022: "Прибыль, тыс. руб. (2022)",
  profit2023: "Прибыль, тыс. руб. (2023)",
  profit2024: "Прибыль, тыс. руб. (2024)",

  // Персонал
  staffTotal2022: "Численность сотрудников (всего) 2022",
  staffTotal2023: "Численность сотрудников (всего) 2023",
  staffTotal2024: "Численность сотрудников (всего) 2024",
  staffMoscow2022: "Численность в Москве 2022",
  staffMoscow2023: "Численность в Москве 2023",
  staffMoscow2024: "Численность в Москве 2024",

  // ФОТ
  payrollTotal2022: "ФОТ всех сотрудников, тыс. руб. (2022)",
  payrollTotal2023: "ФОТ всех сотрудников, тыс. руб. (2023)",
  payrollTotal2024: "ФОТ всех сотрудников, тыс. руб. (2024)",
  payrollMoscow2022: "ФОТ сотрудников Москвы, тыс. руб. (2022)",
  payrollMoscow2023: "ФОТ сотрудников Москвы, тыс. руб. (2023)",
  payrollMoscow2024: "ФОТ сотрудников Москвы, тыс. руб. (2024)",

  // Средняя зарплата
  avgSalaryTotal2022: "Средняя зарплата, тыс. руб. (2022)",
  avgSalaryTotal2023: "Средняя зарплата, тыс. руб. (2023)",
  avgSalaryTotal2024: "Средняя зарплата, тыс. руб. (2024)",
  avgSalaryMoscow2022: "Средняя зарплата (Москва) 2022",
  avgSalaryMoscow2023: "Средняя зарплата (Москва) 2023",
  avgSalaryMoscow2024: "Средняя зарплата (Москва) 2024",

  // Налоги
  taxTotal2022: "Налоги, тыс. руб. (2022)",
  taxTotal2023: "Налоги, тыс. руб. (2023)",
  taxTotal2024: "Налоги, тыс. руб. (2024)",
  taxProfit2022: "Налог на прибыль, тыс. руб. (2022)",
  taxProfit2023: "Налог на прибыль, тыс. руб. (2023)",
  taxProfit2024: "Налог на прибыль, тыс. руб. (2024)",
  taxProperty2022: "Налог на имущество, тыс. руб. (2022)",
  taxProperty2023: "Налог на имущество, тыс. руб. (2023)",
  taxProperty2024: "Налог на имущество, тыс. руб. (2024)",
  taxLand2022: "Налог на землю, тыс. руб. (2022)",
  taxLand2023: "Налог на землю, тыс. руб. (2023)",
  taxLand2024: "Налог на землю, тыс. руб. (2024)",
  taxNdfl2022: "НДФЛ, тыс. руб. (2022)",
  taxNdfl2023: "НДФЛ, тыс. руб. (2023)",
  taxNdfl2024: "НДФЛ, тыс. руб. (2024)",
  taxTransport2022: "Транспортный налог, тыс. руб. (2022)",
  taxTransport2023: "Транспортный налог, тыс. руб. (2023)",
  taxTransport2024: "Транспортный налог, тыс. руб. (2024)",
  taxOther2022: "Прочие налоги, тыс. руб. (2022)",
  taxOther2023: "Прочие налоги, тыс. руб. (2023)",
  taxOther2024: "Прочие налоги, тыс. руб. (2024)",

  // Инвестиции и экспорт
  excise2022: "Акцизы, тыс. руб. (2022)",
  excise2023: "Акцизы, тыс. руб. (2023)",
  excise2024: "Акцизы, тыс. руб. (2024)",
  investMoscow2022: "Инвестиции в Москву, тыс. руб. (2022)",
  investMoscow2023: "Инвестиции в Москву, тыс. руб. (2023)",
  investMoscow2024: "Инвестиции в Москву, тыс. руб. (2024)",
  export2022: "Экспорт, тыс. руб. (2022)",
  export2023: "Экспорт, тыс. руб. (2023)",
  export2024: "Экспорт, тыс. руб. (2024)",
  hasExport: "Наличие экспорта",
  exportPrevYear: "Экспорт за предыдущий год, тыс. руб.",
  exportCountries: "Страны-импортёры",
  // Недвижимость
  landCadastral: "Кадастровый номер ЗУ",
  landArea: "Площадь ЗУ, м²",
  landUse: "Вид разрешённого использования ЗУ",
  landOwnership: "Форма собственности ЗУ",
  landOwner: "Собственник ЗУ",
  oksCadastral: "Кадастровый номер ОКСа",
  oksArea: "Площадь ОКСов, м²",
  oksUse: "Вид разрешённого использования ОКСов",
  oksType: "Тип строения и цель использования",
  oksOwnership: "Форма собственности ОКСов",
  oksOwner: "Собственник ОКСов",
  productionArea: "Площадь производственных помещений, м²",

  // Продукция
  standardizedProduct: "Стандартизированная продукция",
  productNames: "Названия продукции",
  productOkpd2: "Коды ОКПД 2",
  productSegments: "Типы и сегменты продукции",
  productCatalog: "Каталог продукции",
  hasGovOrder: "Наличие госзаказа",
  capacityUtilization: "Загрузка производственных мощностей",

  // Координаты
  legalCoords: "Координаты юр. адреса",
  productionCoords: "Координаты производства",
  additionalCoords: "Координаты доп. площадки",
  latitude: "Широта",
  longitude: "Долгота",

  // География
  okrug: "Округ",
  district: "Район",
};

const CompanyInfo: React.FC = () => {
  const { inn } = useParams<{ inn: string }>();
  const {
    company: { currentCompany, getCompanyByInn, updateCompanyField },
  } = useStores();

  const [editingField, setEditingField] = useState<string | null>(null);
  const [tempValue, setTempValue] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    if (inn) getCompanyByInn(inn);
  }, [inn, getCompanyByInn]);

  const handleCancel = () => setEditingField(null);

  const handleEdit = (key: string, value: string) => {
    setEditingField(key);
    setTempValue(value);
  };

  const handleSave = async (key: string) => {
    if (!inn) return;
    await updateCompanyField(inn, key, tempValue);
    setEditingField(null);
  };

  const filteredData = useMemo(() => {
    if (!currentCompany) return [];
    const entries = Object.entries(currentCompany);
    if (!searchQuery.trim()) return entries;

    const query = searchQuery.toLowerCase();

    return entries.filter(([key, value]) => {
      const translatedKey = fieldDictionary[key]?.toLowerCase() || key.toLowerCase();
      const stringValue = String(value ?? "").toLowerCase();

      return translatedKey.includes(query) || stringValue.includes(query);
    });
  }, [currentCompany, searchQuery]);

  if (!currentCompany || !Object.keys(currentCompany).length)
    return (
      <div className="min-h-screen flex items-center justify-center text-gray-500 text-lg">
        Компания не найдена или данные загружаются...
      </div>
    );

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
        <h1 className="text-3xl font-bold text-gray-800 text-center sm:text-left">
          Информация о компании —{" "}
          <span className="text-blue-600">{currentCompany.orgName}</span>
        </h1>

        <div className="flex gap-3">
          <Link to="/analytics">
            <Button color="blue" className="hover:scale-105 transition">
              📊 Аналитика
            </Button>
          </Link>
          <Link to="/graph">
            <Button color="purple" className="hover:scale-105 transition">
              🔗 Граф
            </Button>
          </Link>
          <Link to="/companies">
            <Button color="light" className="hover:scale-105 transition">
              ← Назад
            </Button>
          </Link>
        </div>
      </div>

      {/* Поиск */}
      <div className="flex items-center gap-3 mb-6">
        <FaSearch className="text-gray-500" />
        <TextInput
          placeholder="Поиск по данным компании..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-96"
        />
        {searchQuery && (
          <Button color="gray" size="sm" onClick={() => setSearchQuery("")}>
            Очистить
          </Button>
        )}
      </div>

      {/* Таблица данных */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="divide-y divide-gray-200">
          {filteredData.map(([key, value]) => (
            <div
              key={key}
              className="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center py-3"
            >
              <span className="font-medium text-gray-600 sm:w-1/3">
                {fieldDictionary[key] ?? key}
              </span>

              <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:w-2/3 mt-2 sm:mt-0">
                {editingField === key ? (
                  <>
                    <TextInput
                      value={tempValue}
                      onChange={(e) => setTempValue(e.target.value)}
                      className="flex-1"
                    />
                    <div className="flex gap-2">
                      <Button
                        color="success"
                        size="sm"
                        onClick={() => handleSave(key)}
                      >
                        Сохранить
                      </Button>
                      <Button color="gray" size="sm" onClick={handleCancel}>
                        Отмена
                      </Button>
                    </div>
                  </>
                ) : (
                  <>
                    <span className="text-gray-800 break-words">
                      {value ?? "-"}
                    </span>
                    <button
                      className="text-gray-400 hover:text-blue-500 transition ml-2"
                      onClick={() => handleEdit(key, String(value))}
                      title="Редактировать"
                    >
                      <FaEdit size={18} />
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
          {filteredData.length === 0 && (
            <p className="text-center text-gray-500 py-6">
              Ничего не найдено по запросу «{searchQuery}»
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default observer(CompanyInfo);
