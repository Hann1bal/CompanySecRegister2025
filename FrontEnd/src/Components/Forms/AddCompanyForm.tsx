import { useState } from "react";
import { Label, TextInput, Select, Button } from "flowbite-react";
import { AiOutlineCloseCircle } from "react-icons/ai";

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

const AddCompanyForm = () => {
  const [addedFields, setAddedFields] = useState<string[]>([]);

  const handleSelect = (value: string) => {
    if (value && !addedFields.includes(value)) {
      setAddedFields([...addedFields, value]);
    }
  };

  const handleRemove = (field: string) => {
    setAddedFields(addedFields.filter((f) => f !== field));
  };

  return (
    <div className="w-full max-w-3xl">
      <form className="flex flex-col gap-5">

        <div>
          <Label htmlFor="inn" value="ИНН *" />
          <TextInput id="inn" placeholder="Введите ИНН" required />
        </div>

        <div>
          <Label htmlFor="orgName" value="Наименование организации *" />
          <TextInput
            id="orgName"
            placeholder="Введите краткое название"
            required
          />
        </div>

        <div>
          <Label
            htmlFor="orgFullName"
            value="Полное наименование организации *"
          />
          <TextInput
            id="orgFullName"
            placeholder="Введите полное название"
            required
          />
        </div>

        <div>
          <Label htmlFor="status" value="Статус *" />
          <TextInput id="status" placeholder="Например: Действующая" required />
        </div>

        <div>
          <Label htmlFor="address" value="Юридический адрес *" />
          <TextInput id="address" placeholder="Введите адрес" required />
        </div>

        {addedFields.length > 0 && (
          <div className="flex flex-col gap-4 mt-2">
            {addedFields.map((field) => (
              <div key={field} className="flex items-center gap-2 transition">
                <div className="flex-1">
                  <Label htmlFor={field}>{field}</Label>
                  <TextInput
                    id={field}
                    placeholder={`Введите ${field.toLowerCase()}`}
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
          </div>
        )}

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
        <Label className="mt-5 text-gray-500" value="Поля, отмеченные звездочкой * - обязательны для заполнения" />
        {/* Кнопки */}
        <div className="flex justify-center gap-4 mt-6">
          <Button color="gray">Отмена</Button>
          <Button color="success">Добавить</Button>
        </div>
      </form>
    </div>
  );
};

export default AddCompanyForm;
