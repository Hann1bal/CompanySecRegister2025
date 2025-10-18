import { useState } from "react";
import { Label, TextInput, Select, Button } from "flowbite-react";
import { AiOutlineCloseCircle } from "react-icons/ai";
import { useStores } from "../../context/root-store-context";
import { ICompany } from "../../Interfaces/ICompany";

interface AddCompanyFormProps {
  onCloseModalAction: (state: boolean) => void;
}

const allExtraFields = [
  "Адрес производства",
  "Адрес дополнительной площадки",
  "Основная отрасль",
  "Подотрасль (Основная)",
  "Основной ОКВЭД",
  "Вид деятельности по основному ОКВЭД",
  "Производственный ОКВЭД",
  "Дата регистрации",
  "Руководитель",
  "Головная организация",
  "ИНН головной организации",
  "Контактные данные руководства",
  "Контакт сотрудника организации",
  "Контактные данные ответственного по ЧС",
  "Сайт",
  "Электронная почта",
  "Данные об оказанных мерах поддержки",
  "Наличие особого статуса",
  "Статус МСП",
];

const AddCompanyForm = ({ onCloseModalAction }: AddCompanyFormProps) => {
  const {
    company: { createCompany },
  } = useStores();

  // локальное состояние полей
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [addedFields, setAddedFields] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSelect = (value: string) => {
    if (value && !addedFields.includes(value)) {
      setAddedFields([...addedFields, value]);
    }
  };

  const handleRemove = (field: string) => {
    setAddedFields(addedFields.filter((f) => f !== field));
    setFormData((prev) => {
      const updated = { ...prev };
      delete updated[field];
      return updated;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

      const company: ICompany = {
        inn: formData["ИНН"] || "",
        orgName: formData["Наименование организации"] || "",
        orgFullName: formData["Полное наименование организации"] || "",
        status: formData["Статус"] || "",
        legalAddress: formData["Юридический адрес"] || "",
        productionAddress: formData["Адрес производства"] || "",
        additionalSiteAddress: formData["Адрес дополнительной площадки"] || "",
        industry: formData["Основная отрасль"] || "",
        subIndustry: formData["Подотрасль (Основная)"] || "",
        mainOkved: formData["Основной ОКВЭД"] || "",
        mainOkvedActivity:
          formData["Вид деятельности по основному ОКВЭД"] || "",
        productionOkved: formData["Производственный ОКВЭД"] || "",
        registrationDate: formData["Дата регистрации"] || "",
        head: formData["Руководитель"] || "",
        parentOrgName: formData["Головная организация"] || "",
        parentOrgInn: Number(formData["ИНН головной организации"]) || 0,
        managementContacts: formData["Контактные данные руководства"] || "",
        orgContact: formData["Контакт сотрудника организации"] || "",
        emergencyContact:
          formData["Контактные данные ответственного по ЧС"] || "",
        website: formData["Сайт"] || "",
        email: formData["Электронная почта"] || "",
        supportMeasures:
          formData["Данные об оказанных мерах поддержки"] || "",
        specialStatus: formData["Наличие особого статуса"] || "",
        smeStatus: formData["Статус МСП"] || "",
      };

      const ok = await createCompany(company);

  };

  return (
    <div className="w-full max-w-3xl">
      <form className="flex flex-col gap-5" onSubmit={handleSubmit}>
        {/* Обязательные поля */}
        <div>
          <Label htmlFor="inn" value="ИНН *" />
          <TextInput
            id="inn"
            required
            placeholder="Введите ИНН"
            onChange={(e) => handleChange("ИНН", e.target.value)}
          />
        </div>

        <div>
          <Label htmlFor="orgName" value="Наименование организации *" />
          <TextInput
            id="orgName"
            required
            placeholder="Введите краткое название"
            onChange={(e) =>
              handleChange("Наименование организации", e.target.value)
            }
          />
        </div>

        <div>
          <Label
            htmlFor="orgFullName"
            value="Полное наименование организации *"
          />
          <TextInput
            id="orgFullName"
            required
            placeholder="Введите полное название"
            onChange={(e) =>
              handleChange("Полное наименование организации", e.target.value)
            }
          />
        </div>

        <div>
          <Label htmlFor="status" value="Статус *" />
          <TextInput
            id="status"
            required
            placeholder="Например: Действующая"
            onChange={(e) => handleChange("Статус", e.target.value)}
          />
        </div>

        <div>
          <Label htmlFor="address" value="Юридический адрес *" />
          <TextInput
            id="address"
            required
            placeholder="Введите адрес"
            onChange={(e) => handleChange("Юридический адрес", e.target.value)}
          />
        </div>

        {/* Дополнительные поля */}
        {addedFields.map((field) => (
          <div key={field} className="flex items-center gap-2">
            <div className="flex-1">
              <Label htmlFor={field}>{field}</Label>
              <TextInput
                id={field}
                placeholder={`Введите ${field.toLowerCase()}`}
                onChange={(e) => handleChange(field, e.target.value)}
              />
            </div>
            <button
              type="button"
              onClick={() => handleRemove(field)}
              className="text-red-500 hover:text-red-700 transition"
            >
              <AiOutlineCloseCircle size={22} />
            </button>
          </div>
        ))}

        <div>
          <Label value="Добавить дополнительное поле" />
          <Select
            id="extraField"
            onChange={(e) => handleSelect(e.target.value)}
            className="mt-2"
          >
            <option value="">Выберите поле...</option>
            {allExtraFields.map((field) => (
              <option key={field} value={field}>
                {field}
              </option>
            ))}
          </Select>
        </div>

        {error && <p className="text-red-600 text-center mt-2">{error}</p>}

        <Label
          className="mt-5 text-gray-500"
          value="Поля со * обязательны для заполнения"
        />

        {/* Кнопки */}
        <div className="flex justify-center gap-4 mt-6">
          <Button
            type="button"
            onClick={() => onCloseModalAction(false)}
            color="gray"
            disabled={loading}
          >
            Отмена
          </Button>
          <Button type="submit" color="success" disabled={loading}>
            {loading ? "Сохранение..." : "Добавить"}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default AddCompanyForm;
