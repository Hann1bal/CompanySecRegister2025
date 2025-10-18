import React, { useState } from "react";
import { Button, Card } from "flowbite-react";
import ReactECharts from "echarts-for-react";

export default function CompanyAnalyticsPage() {
  const [reportType, setReportType] = useState("finance");

  // 💰 Данные для финансовых отчётов
  const financeData = {
    revenue: { years: ["2020", "2021", "2022", "2023", "2024"], data: [4200, 5100, 6000, 7200, 8500] },
    profit: { years: ["2021", "2022", "2023"], data: [780, 910, 1005] },
    taxes: { years: ["2022", "2023", "2024"], data: [1180, 1390, 1500] },
    investments: { years: ["2019", "2020", "2021", "2022"], data: [300, 500, 900, 1400] },
    salary: { years: ["2020", "2021", "2022", "2023", "2024"], data: [58, 63, 69, 74, 80] },
    staff: { years: ["2021", "2022", "2023", "2024"], data: [210, 230, 250, 270] },
  };

  // Основные графики по финансовым направлениям
  const financeCharts = [
    {
      title: "💰 Выручка предприятия",
      color: "#2563EB",
      unit: "тыс. руб.",
      data: financeData.revenue,
    },
    {
      title: "📈 Чистая прибыль (убыток)",
      color: "#16A34A",
      unit: "тыс. руб.",
      data: financeData.profit,
    },
    {
      title: "🧾 Налоговые отчисления",
      color: "#F59E0B",
      unit: "тыс. руб.",
      data: financeData.taxes,
    },
    {
      title: "💼 Инвестиции в развитие",
      color: "#8B5CF6",
      unit: "тыс. руб.",
      data: financeData.investments,
    },
    {
      title: "👷 Средняя заработная плата",
      color: "#10B981",
      unit: "тыс. руб.",
      data: financeData.salary,
    },
    {
      title: "👥 Среднесписочная численность персонала",
      color: "#3B82F6",
      unit: "чел.",
      data: financeData.staff,
    },
  ];

  // 🥧 Круговые диаграммы по годам (структура налогов, прибыли и т.д.)
  const yearlyPieCharts = [
    {
      year: "2022",
      data: [
        { value: 620, name: "Налог на прибыль" },
        { value: 380, name: "НДФЛ" },
        { value: 250, name: "Имущественный" },
        { value: 180, name: "Транспортный" },
        { value: 70, name: "Прочие" },
      ],
    },
    {
      year: "2023",
      data: [
        { value: 740, name: "Налог на прибыль" },
        { value: 420, name: "НДФЛ" },
        { value: 260, name: "Имущественный" },
        { value: 190, name: "Транспортный" },
        { value: 90, name: "Прочие" },
      ],
    },
    {
      year: "2024",
      data: [
        { value: 800, name: "Налог на прибыль" },
        { value: 440, name: "НДФЛ" },
        { value: 280, name: "Имущественный" },
        { value: 210, name: "Транспортный" },
        { value: 100, name: "Прочие" },
      ],
    },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* 🔹 Верхняя панель */}
      <header className="flex justify-between items-center bg-white shadow px-8 py-4 w-full">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            Аналитика компании «ООО ТехПром»
          </h1>
          <p className="text-gray-500">ИНН: 7701234567</p>
        </div>
        <Button color="light" className="hover:scale-105 transition">
          ⬅ Назад
        </Button>
      </header>

      {/* 🔹 Основной контент */}
      <div className="flex flex-1 p-6 gap-6">
        <div className="flex flex-col flex-1 gap-4">
          {/* Кнопки выбора отчётности */}
          <Card className="p-4 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-700 mb-2">
              Выберите тип отчётности
            </h2>
            <div className="flex flex-wrap gap-5">
              <Button
                size="sm"
                color="blue"
                className="font-semibold scale-105"
              >
                💼 Финансовая отчётность
              </Button>
            </div>
          </Card>

          {/* 📊 Групповой блок с финансовыми графиками */}
          <Card className="flex flex-col gap-8 p-6 shadow-md">
            <h2 className="text-xl font-bold text-gray-800 mb-2 text-center">
              Финансовая динамика предприятия (2020–2024)
            </h2>

            {/* Все графики в одной сетке */}
            <div className="grid grid-cols-2 gap-8">
              {financeCharts.map((chart) => (
                <ReactECharts
                  key={chart.title}
                  option={{
                    title: {
                      text: chart.title,
                      left: "center",
                      textStyle: { fontSize: 16, fontWeight: "bold" },
                    },
                    tooltip: { trigger: "axis" },
                    xAxis: { type: "category", data: chart.data.years },
                    yAxis: { type: "value", name: chart.unit },
                    series: [
                      {
                        data: chart.data.data,
                        type: "bar",
                        color: chart.color,
                        barWidth: "60%",
                        label: {
                          show: true,
                          position: "top",
                          formatter: (p: any) => `${p.value} ${chart.unit}`,
                          fontSize: 10,
                        },
                      },
                    ],
                  }}
                  style={{ height: "300px", width: "100%" }}
                />
              ))}
            </div>

            {/* 🔸 Круговые диаграммы по годам */}
            <h2 className="text-lg font-semibold text-gray-700 text-center mt-6">
              Структура налоговых отчислений по годам
            </h2>
            <div className="grid grid-cols-3 gap-6">
              {yearlyPieCharts.map((pie) => (
                <ReactECharts
                  key={pie.year}
                  option={{
                    title: {
                      text: `Налоги ${pie.year}`,
                      left: "center",
                      textStyle: { fontSize: 14, fontWeight: "bold" },
                    },
                    tooltip: {
                      trigger: "item",
                      formatter: "{b}: {c} тыс. руб. ({d}%)",
                    },
                    legend: { bottom: 0, left: "center" },
                    series: [
                      {
                        type: "pie",
                        radius: ["40%", "70%"],
                        itemStyle: {
                          borderRadius: 8,
                          borderColor: "#fff",
                          borderWidth: 2,
                        },
                        label: { show: true, formatter: "{b}: {d}%" },
                        data: pie.data,
                      },
                    ],
                  }}
                  style={{ height: "300px", width: "100%" }}
                />
              ))}
            </div>
          </Card>
        </div>

        {/* Правая колонка (отрасль и финансы) */}
        <div className="w-96 flex flex-col gap-4">
          <Card className="shadow-md">
            <h2 className="text-xl font-semibold text-gray-800 mb-3">
              🏭 Отрасль компании
            </h2>
            <p className="text-gray-700 mb-2">
              <strong>Название:</strong> Машиностроение
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Подотрасль:</strong> Промышленное оборудование
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Количество компаний:</strong> 152
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Средняя выручка:</strong> 7.2 млрд руб.
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Инвестиции 2024:</strong> 1.1 млрд руб.
            </p>
            <p className="text-gray-600 mt-4 text-sm">
              Отрасль демонстрирует стабильный рост, основной фокус —
              модернизация оборудования и экспортная экспансия.
            </p>
          </Card>

          <Card className="shadow-md">
            <h2 className="text-xl font-semibold text-gray-800 mb-3">
              👤 Руководство и Финансы
            </h2>
            <p className="text-gray-700 mb-2">
              <strong>Генеральный директор:</strong> Иванов И.И.
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Управляющий:</strong> Петров С.С.
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Учредитель:</strong> ООО «ИнвестПромГрупп»
            </p>
            <div className="mt-3 border-t pt-3">
              <p className="text-gray-700 mb-2">
                <strong>Финансовое состояние:</strong> Стабильное ✅
              </p>
              <p className="text-gray-700 mb-2">
                <strong>Устойчивость:</strong> Высокая 📈
              </p>
              <p className="text-gray-700 mb-2">
                <strong>Риски:</strong> Низкие ⚡
              </p>
              <p className="text-gray-600 text-sm mt-2">
                Компания демонстрирует устойчивую прибыльность и низкий уровень
                долговой нагрузки.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
