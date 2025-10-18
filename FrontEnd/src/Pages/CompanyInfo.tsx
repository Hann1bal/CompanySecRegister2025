import React, { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Button, TextInput } from "flowbite-react";
import { FaEdit } from "react-icons/fa";

const initialCompanyData = {
  ИНН: "7701234567",
  "Наименование организации": "ООО ТехПром",
  "Полное наименование организации":
    "Общество с ограниченной ответственностью ТехПром",
  Статус: "Действующая",
  "Юридический адрес": "г. Москва, ул. Тверская, д. 10",
  "Адрес производства": "г. Москва, ул. Ленина, д. 15",
  "Основная отрасль": "Машиностроение",
  "Подотрасль (Основная)": "Промышленное оборудование",
  "Дата регистрации": "15.03.2012",
  Руководитель: "Иванов И.И.",
  "Электронная почта": "info@techprom.ru",
  Сайт: "https://techprom.ru",
};

const CompanyInfo: React.FC = () => {
  const { inn } = useParams();
  const [companyData, setCompanyData] = useState(initialCompanyData);
  const [editingField, setEditingField] = useState<string | null>(null);
  const [tempValue, setTempValue] = useState("");

  const handleEdit = (key: string, value: string) => {
    setEditingField(key);
    setTempValue(value);
  };

  const handleSave = (key: string) => {
    setCompanyData({ ...companyData, [key]: tempValue });
    setEditingField(null);
  };

  const handleCancel = () => {
    setEditingField(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Заголовок и панель кнопок */}
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
          <Link to="/">
            <Button color="light" className="hover:scale-105 transition">
              ← Назад
            </Button>
          </Link>
        </div>
      </div>

      {/* Карточка с данными */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="divide-y divide-gray-200">
          {Object.entries(companyData).map(([key, value]) => (
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
        </div>
      </div>
    </div>
  );
};

export default CompanyInfo;
