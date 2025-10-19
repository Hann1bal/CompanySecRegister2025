import React, { useState } from "react";
import { FileInput, Label, Button } from "flowbite-react";
import { useStores } from "../../context/root-store-context";

export const UploadFileForm: React.FC = () => {
  const {
    company: { importCompaniesFromExcel },
  } = useStores();

  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) setFile(selected);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Выберите файл .xlsx или .xls");
      return;
    }

    setIsUploading(true);
    try {
      await importCompaniesFromExcel(file);
      alert("✅ Файл успешно загружен!");
      setFile(null);
    } catch (err) {
      console.error("Ошибка при загрузке:", err);
      alert("❌ Ошибка при загрузке файла");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col w-full items-center justify-center p-6 bg-white rounded-lg shadow-md">
      <Label
        htmlFor="dropzone-file"
        className="flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100"
      >
        <div className="flex flex-col items-center justify-center pb-6 pt-5">
          <svg
            className="mb-4 h-8 w-8 text-gray-500"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 20 16"
          >
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
            />
          </svg>
          <p className="mb-2 text-sm text-gray-500">
            <span className="font-semibold">Кликните для выбора</span> или перетащите файл
          </p>
          <p className="text-xs text-gray-500">Форматы: .xlsx, .xls</p>
        </div>
        <FileInput
          id="dropzone-file"
          className="hidden"
          onChange={handleFileChange}
          accept=".xlsx,.xls"
        />
      </Label>

      {file && (
        <p className="mt-4 text-gray-700 text-sm">
          Выбран файл: <span className="font-medium">{file.name}</span>
        </p>
      )}

      <Button
        color="success"
        className="mt-6 w-full sm:w-1/2"
        onClick={handleUpload}
        disabled={isUploading}
      >
        {isUploading ? "Загрузка..." : "Загрузить"}
      </Button>
    </div>
  );
};
