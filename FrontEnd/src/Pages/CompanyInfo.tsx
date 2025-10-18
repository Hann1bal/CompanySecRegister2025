import React, { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { Button, TextInput } from "flowbite-react";
import { FaEdit, FaSearch } from "react-icons/fa";

const initialCompanyData = {
  ИНН: "7701234567",
  "Наименование организации": "ООО ТехПром",
  "Полное наименование организации": "Общество с ограниченной ответственностью ТехПром",
  Статус: "Действующая",
  "Юридический адрес": "г. Москва, ул. Тверская, д. 10",
  "Адрес производства": "г. Москва, ул. Ленина, д. 15",
  "Адрес дополнительной площадки": "",
  "Основная отрасль": "Машиностроение",
  "Подотрасль (Основная)": "Промышленное оборудование",
  "Основной ОКВЭД": "",
  "Вид деятельности по основному ОКВЭД": "",
  "Производственный ОКВЭД": "",
  "Дата регистрации": "15.03.2012",
  Руководитель: "Иванов И.И.",
  "Головная организация": "",
  "ИНН головной организации": "",
  "Контактные данные руководства": "",
  "Контакт сотрудника организации": "",
  "Контактные данные ответственного по ЧС": "",
  Сайт: "https://techprom.ru",
  "Электронная почта": "info@techprom.ru",
  "Данные об оказанных мерах поддержки": "",
  "Наличие особого статуса": "",
  "Статус МСП": "",
  "Выручка предприятия, тыс. руб. 2022": "",
  "Выручка предприятия, тыс. руб. 2023": "",
  "Выручка предприятия, тыс. руб. 2024": "",
  "Чистая прибыль (убыток), тыс. руб. 2022": "",
  "Чистая прибыль (убыток), тыс. руб. 2023": "",
  "Чистая прибыль (убыток), тыс. руб. 2024": "",
  "Среднесписочная численность персонала (всего по компании), чел 2022": "",
  "Среднесписочная численность персонала (всего по компании), чел 2023": "",
  "Среднесписочная численность персонала (всего по компании), чел 2024": "",
  "Среднесписочная численность персонала, работающего в Москве, чел 2022": "",
  "Среднесписочная численность персонала, работающего в Москве, чел 2023": "",
  "Среднесписочная численность персонала, работающего в Москве, чел 2024": "",
  "Фонд оплаты труда всех сотрудников организации, тыс. руб 2022": "",
  "Фонд оплаты труда всех сотрудников организации, тыс. руб 2023": "",
  "Фонд оплаты труда всех сотрудников организации, тыс. руб 2024": "",
  "Фонд оплаты труда сотрудников, работающих в Москве, тыс. руб. 2022": "",
  "Фонд оплаты труда сотрудников, работающих в Москве, тыс. руб. 2023": "",
  "Фонд оплаты труда сотрудников, работающих в Москве, тыс. руб. 2024": "",
  "Средняя з.п. всех сотрудников организации, тыс.руб. 2022": "",
  "Средняя з.п. всех сотрудников организации, тыс.руб. 2023": "",
  "Средняя з.п. всех сотрудников организации, тыс.руб. 2024": "",
  "Средняя з.п. сотрудников, работающих в Москве, тыс.руб. 2022": "",
  "Средняя з.п. сотрудников, работающих в Москве, тыс.руб. 2023": "",
  "Средняя з.п. сотрудников, работающих в Москве, тыс.руб. 2024": "",
  "Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2022": "",
  "Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2023": "",
  "Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2024": "",
  "Налог на прибыль, тыс.руб. 2022": "",
  "Налог на прибыль, тыс.руб. 2023": "",
  "Налог на прибыль, тыс.руб. 2024": "",
  "Налог на имущество, тыс.руб. 2022": "",
  "Налог на имущество, тыс.руб. 2023": "",
  "Налог на имущество, тыс.руб. 2024": "",
  "Налог на землю, тыс.руб. 2022": "",
  "Налог на землю, тыс.руб. 2023": "",
  "Налог на землю, тыс.руб. 2024": "",
  "НДФЛ, тыс.руб. 2022": "",
  "НДФЛ, тыс.руб. 2023": "",
  "НДФЛ, тыс.руб. 2024": "",
  "Транспортный налог, тыс.руб. 2022": "",
  "Транспортный налог, тыс.руб. 2023": "",
  "Транспортный налог, тыс.руб. 2024": "",
  "Прочие налоги 2022": "",
  "Прочие налоги 2023": "",
  "Прочие налоги 2024": "",
  "Акцизы, тыс. руб. 2022": "",
  "Акцизы, тыс. руб. 2023": "",
  "Акцизы, тыс. руб. 2024": "",
  "Инвестиции в Мск 2022 тыс. руб.": "",
  "Инвестиции в Мск 2023 тыс. руб.": "",
  "Инвестиции в Мск 2024 тыс. руб.": "",
  "Объем экспорта, тыс. руб. 2022": "",
  "Объем экспорта, тыс. руб. 2023": "",
  "Объем экспорта, тыс. руб. 2024": "",
  "Кадастровый номер ЗУ": "",
  "Площадь ЗУ": "",
  "Вид разрешенного использования ЗУ": "",
  "Вид собственности ЗУ": "",
  "Собственник ЗУ": "",
  "Кадастровый номер ОКСа": "",
  "Площадь ОКСов": "",
  "Вид разрешенного использования ОКСов": "",
  "Тип строения и цель использования": "",
  "Вид собственности ОКСов": "",
  "Собственник ОКСов": "",
  "Площадь производственных помещений, кв.м.": "",
  "Стандартизированная продукция": "",
  "Название (виды производимой продукции)": "",
  "Перечень производимой продукции по кодам ОКПД 2": "",
  "Перечень производимой продукции по типам и сегментам": "",
  "Каталог продукции": "",
  "Наличие госзаказа": "",
  "Уровень загрузки производственных мощностей": "",
  "Наличие поставок продукции на экспорт": "",
  "Объем экспорта (млн руб.) за предыдущий календарный год": "",
  "Перечень государств-импортеров": "",
  "Координаты юридического адреса": "",
  "Координаты адреса производства": "",
  "Координаты адреса дополнительной площадки": "",
  "Координаты (широта)": "",
  "Координаты (долгота)": "",
  Округ: "",
  Район: "",
};


const CompanyInfo: React.FC = () => {
  const [companyData, setCompanyData] = useState(initialCompanyData);
  const [editingField, setEditingField] = useState<string | null>(null);
  const [tempValue, setTempValue] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  const handleEdit = (key: string, value: string) => {
    setEditingField(key);
    setTempValue(value);
  };

  const handleSave = (key: string) => {
    setCompanyData({ ...companyData, [key]: tempValue });
    setEditingField(null);
  };

  const handleCancel = () => setEditingField(null);

  /** Фильтрация данных по поисковому запросу */
  const filteredData = useMemo(() => {
    if (!searchQuery.trim()) return Object.entries(companyData);
    const query = searchQuery.toLowerCase();
    return Object.entries(companyData).filter(
      ([key, value]) =>
        key.toLowerCase().includes(query) ||
        String(value).toLowerCase().includes(query)
    );
  }, [companyData, searchQuery]);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Навбар и панель действий */}
      <div className="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
        <h1 className="text-3xl font-bold text-gray-800 text-center sm:text-left">
          Информация о компании —{" "}
          <span className="text-blue-600">
            {companyData["Наименование организации"]}
          </span>
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

      {/* Поле поиска */}
      <div className="flex items-center gap-3 mb-6">
        <FaSearch className="text-gray-500" />
        <TextInput
          placeholder="Поиск по данным компании..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-96"
        />
        {searchQuery && (
          <Button
            color="gray"
            size="sm"
            onClick={() => setSearchQuery("")}
          >
            Очистить
          </Button>
        )}
      </div>

      {/* Секция с данными */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="divide-y divide-gray-200">
          {filteredData.map(([key, value]) => (
            <div
              key={key}
              className="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center py-3 group"
            >
              <div className="flex items-center gap-2 sm:w-1/3">
                <span className="font-medium text-gray-600">{key}</span>
              </div>

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
                      {value || "-"}
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

export default CompanyInfo;
