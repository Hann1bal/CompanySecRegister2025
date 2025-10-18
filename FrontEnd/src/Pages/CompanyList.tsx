import React, { useEffect, useState } from "react";
import { Table, TextInput, Button } from "flowbite-react";
import AddCompModal from "../Components/Modals/AddCompModal";
import ImportFromFile from "../Components/Modals/ImportFromFile";
import { useNavigate } from "react-router";
import { useStores } from "../context/root-store-context";
import { observer } from "mobx-react-lite";

const CompaniesListPage: React.FC = () => {
  const {
    company: { data, getData },
  } = useStores();

  const [addCompanyModal, setAddCompanyModal] = useState(false);
  const [openModal, setOpenModal] = useState(false);
  const navigate = useNavigate();

  // --- Фильтры ---
  const [filters, setFilters] = useState({
    inn: "",
    orgName: "",
    orgFullName: "",
    status: "",
    address: "",
  });

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  // --- Получение данных ---
  useEffect(() => {
    getData();
  }, [getData]);

  // --- Фильтрация данных ---
  const filteredData = data.filter((c) => {
    const matchesInn = c.inn?.toString().toLowerCase().includes(filters.inn.toLowerCase());
    const matchesName = c.orgName?.toLowerCase().includes(filters.orgName.toLowerCase());
    const matchesFullName = c.orgFullName?.toLowerCase().includes(filters.orgFullName.toLowerCase());
    const matchesStatus = c.status?.toLowerCase().includes(filters.status.toLowerCase());
    const matchesAddress = c.legalAddress?.toLowerCase().includes(filters.address.toLowerCase());
    return matchesInn && matchesName && matchesFullName && matchesStatus && matchesAddress;
  });

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Заголовок и кнопки */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Список Московских Компаний</h1>

        <div className="flex gap-3">
          <Button
            color="info"
            className="shadow-md hover:scale-105 transition-transform duration-200"
            onClick={() => navigate("/mskanalytics")}
          >
            📊 Аналитика отраслей Москвы
          </Button>

          <Button
            color="success"
            className="shadow-md hover:scale-105 transition-transform duration-200"
            onClick={() => setOpenModal(true)}
          >
            + Импорт из файла
          </Button>

          <Button
            color="success"
            className="shadow-md hover:scale-105 transition-transform duration-200"
            onClick={() => setAddCompanyModal(true)}
          >
            + Добавить организацию
          </Button>
        </div>
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
                  onChange={(e) => handleFilterChange("orgName", e.target.value)}
                />
              </Table.Cell>
              <Table.Cell>
                <TextInput
                  placeholder="Поиск..."
                  value={filters.orgFullName}
                  onChange={(e) => handleFilterChange("orgFullName", e.target.value)}
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
                  onChange={(e) => handleFilterChange("address", e.target.value)}
                />
              </Table.Cell>
              <Table.Cell></Table.Cell>
            </Table.Row>

            {/* Данные */}
            {filteredData.length > 0 ? (
              filteredData.map((company) => (
                <Table.Row key={company.orgFullName} className="bg-white hover:bg-gray-50">
                  <Table.Cell>{company.orgFullName}</Table.Cell>
                  <Table.Cell>{company.orgName}</Table.Cell>
                  <Table.Cell>-</Table.Cell>
                  <Table.Cell>{company.status}</Table.Cell>
                  <Table.Cell>{company.legalAddress}</Table.Cell>
                  <Table.Cell>
                    <Button
                      color="blue"
                      size="sm"
                      pill
                      className="shadow-md hover:scale-105 transition-transform duration-200"
                      onClick={() => navigate(`/company/${company.orgFullName}`, {state: company.orgFullName})}
                    >
                      Подробнее
                    </Button>
                  </Table.Cell>
                </Table.Row>
              ))
            ) : (
              <Table.Row>
                <Table.Cell colSpan={6} className="text-center text-gray-500 py-6">
                  Компаний не найдено
                </Table.Cell>
              </Table.Row>
            )}
          </Table.Body>
        </Table>
      </div>

      {/* Модальные окна */}
      <AddCompModal show={addCompanyModal} switchState={setAddCompanyModal} />
      <ImportFromFile show={openModal} switchState={setOpenModal} />
    </div>
  );
};

export default observer(CompaniesListPage);
