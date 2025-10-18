import React, { useMemo } from "react";
import ReactECharts from "echarts-for-react";
import { Button, Card } from "flowbite-react";

export default function MoscowIndustryAnalytics() {
  /** Данные по годам и отраслям */
  const data = {
    "Машиностроение": {
      years: ["2022", "2023", "2024"],
      companies: [120, 135, 150],
      employees: [35000, 37000, 41000],
      revenue: [85, 95, 110],
    },
    IT: {
      years: ["2022", "2023", "2024"],
      companies: [180, 210, 250],
      employees: [48000, 52000, 57000],
      revenue: [140, 170, 200],
    },
    "Пищевая промышленность": {
      years: ["2022", "2023", "2024"],
      companies: [95, 100, 120],
      employees: [15000, 16000, 19000],
      revenue: [45, 52, 65],
    },
    "Строительство": {
      years: ["2022", "2023", "2024"],
      companies: [140, 160, 180],
      employees: [27000, 30000, 32000],
      revenue: [70, 80, 92],
    },
    Энергетика: {
      years: ["2022", "2023", "2024"],
      companies: [110, 130, 145],
      employees: [31000, 34000, 36000],
      revenue: [120, 135, 155],
    },
    "Финансы": {
      years: ["2022", "2023", "2024"],
      companies: [60, 85, 95],
      employees: [21000, 25000, 28000],
      revenue: [130, 155, 180],
    },
  };

  /** Конфигурации для всех графиков */
  const charts = useMemo(() => {
    const makeChart = (industry: string, d: any) => ({
      title: { text: industry, left: "center" },
      tooltip: { trigger: "axis" },
      legend: {
        bottom: 0,
        data: ["Предприятия", "Сотрудники", "Выручка"],
      },
      xAxis: { type: "category", data: d.years },
      yAxis: { type: "value" },
      series: [
        {
          name: "Предприятия",
          type: "bar",
          data: d.companies,
          barWidth: "20%",
          itemStyle: { color: "#2563EB" },
          label: { show: true, position: "top", formatter: "{c} шт." },
        },
        {
          name: "Сотрудники",
          type: "bar",
          data: d.employees.map((v: number) => v / 1000),
          barWidth: "20%",
          itemStyle: { color: "#10B981" },
          label: { show: true, position: "top", formatter: "{c} тыс." },
        },
        {
          name: "Выручка",
          type: "line",
          smooth: true,
          data: d.revenue,
          itemStyle: { color: "#F59E0B" },
          label: { show: true, position: "top", formatter: "{c} млрд ₽" },
        },
      ],
    });

    return Object.entries(data).map(([industry, d]) =>
      makeChart(industry, d)
    );
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Навбар */}
      <div className="flex justify-between items-center bg-white shadow px-8 py-4">
        <h1 className="text-2xl font-bold text-gray-800">
          Исследование отраслей Москвы
        </h1>
        <Button color="light" onClick={() => window.history.back()}>
          ← Назад к списку компаний
        </Button>
      </div>

      {/* Графики */}
      <div className="grid grid-cols-2 gap-6 p-6">
        {charts.map((chart, idx) => (
          <Card key={idx} className="shadow-md">
            <ReactECharts option={chart} style={{ height: "420px", width: "100%" }} />
          </Card>
        ))}
      </div>
    </div>
  );
}
