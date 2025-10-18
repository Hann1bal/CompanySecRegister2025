import React, { useState } from "react";
import { Table, TextInput, Button } from "flowbite-react";
import AddCompModal from "../Components/Modals/AddCompModal";
import { useNavigate } from "react-router";

interface Company {
  inn: string;
  orgName: string;
  orgFullName: string;
  status: string;
  address: string;
}

const companyData = {
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

const initialData: Company[] = [
  {
    inn: "7701234567",
    orgName: "ООО ТехПром",
    orgFullName: "Общество с ограниченной ответственностью ТехПром",
    status: "Действующая",
    address: "г. Москва, ул. Тверская, д. 10",
  },
  {
    inn: "7723456789",
    orgName: "АО МосЭнерго",
    orgFullName: "Акционерное общество Московская Энергия",
    status: "Действующая",
    address: "г. Москва, ул. Ленина, д. 15",
  },
];

const CompaniesListPage: React.FC = () => {
  const [addCompanyModal, setaddCompanyModal] = useState<boolean>(false);
  const navigate = useNavigate();

  const [filters, setFilters] = useState({
    inn: "",
    orgName: "",
    orgFullName: "",
    status: "",
    address: "",
  });

  const handleFilterChange = (key: string, value: string) => {
    setFilters({ ...filters, [key]: value });
  };

  const filteredData = initialData.filter((c) =>
    Object.entries(filters).every(([key, value]) =>
      c[key as keyof Company].toLowerCase().includes(value.toLowerCase())
    )
  );

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Заголовок и кнопка */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Список Московских Компаний
        </h1>

        <Button
          color="success"
          className="shadow-md hover:scale-105 transition-transform duration-200"
          onClick={() => setaddCompanyModal(true)}
        >
          + Добавить организацию
        </Button>
      </div>

      {/* Таблица */}
      <div className="overflow-x-auto shadow-lg rounded-lg bg-white">
        <Table>
          <Table.Head>
            <Table.HeadCell>ИНН</Table.HeadCell>
            <Table.HeadCell>Наименование организации</Table.HeadCell>
            <Table.HeadCell>Полное наименование организации</Table.HeadCell>
            <Table.HeadCell>Статус</Table.HeadCell>
            <Table.HeadCell>Юридический адрес</Table.HeadCell>
            <Table.HeadCell>Подробнее</Table.HeadCell>
          </Table.Head>

          <Table.Body className="divide-y">
            {/* Фильтры */}
            <Table.Row className="bg-gray-100">
              <Table.Cell>
                <TextInput
                  placeholder="Поиск..."
                  value={filters.inn}
                  onChange={(e) => handleFilterChange("inn", e.target.value)}
                />
              </Table.Cell>
              <Table.Cell>
                <TextInput
                  placeholder="Поиск..."
                  value={filters.orgName}
                  onChange={(e) =>
                    handleFilterChange("orgName", e.target.value)
                  }
                />
              </Table.Cell>
              <Table.Cell>
                <TextInput
                  placeholder="Поиск..."
                  value={filters.orgFullName}
                  onChange={(e) =>
                    handleFilterChange("orgFullName", e.target.value)
                  }
                />
              </Table.Cell>
              <Table.Cell>
                <TextInput
                  placeholder="Поиск..."
                  value={filters.status}
                  onChange={(e) => handleFilterChange("status", e.target.value)}
                />
              </Table.Cell>
              <Table.Cell>
                <TextInput
                  placeholder="Поиск..."
                  value={filters.address}
                  onChange={(e) =>
                    handleFilterChange("address", e.target.value)
                  }
                />
              </Table.Cell>
              <Table.Cell></Table.Cell>
            </Table.Row>

            {/* Данные */}
            {filteredData.map((company) => (
              <Table.Row
                key={company.inn}
                className="bg-white hover:bg-gray-50"
              >
                <Table.Cell>{company.inn}</Table.Cell>
                <Table.Cell>{company.orgName}</Table.Cell>
                <Table.Cell>{company.orgFullName}</Table.Cell>
                <Table.Cell>{company.status}</Table.Cell>
                <Table.Cell>{company.address}</Table.Cell>
                <Table.Cell>
                  <Button
                    color="blue"
                    size="sm"
                    pill
                    className="shadow-md hover:scale-105 transition-transform duration-200"
                    onClick={() => navigate(`/company/${company.inn}`)}
                  >
                    Подробнее
                  </Button>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </div>
      <AddCompModal
        show={addCompanyModal}
        switchState={setaddCompanyModal}
      ></AddCompModal>
    </div>
  );
};

export default CompaniesListPage;
