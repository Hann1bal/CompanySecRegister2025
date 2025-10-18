import React, { useMemo, useRef, useState } from "react";
import ReactECharts from "echarts-for-react";
import { Button, Card } from "flowbite-react";

/** Типы */
type Staff = { id: string; name: string; role: string };
type Company = { id: string; name: string; staff: Staff[] };
type Sector = { id: string; name: string; companies: Company[] };

/** Демо-данные */
const SECTORS: Sector[] = [
  {
    id: "okved_28",
    name: "28 — Машиностроение",
    companies: [
      {
        id: "ntc",
        name: "НТЦ Приводная техника",
        staff: [
          { id: "tatneft", name: "Татнефть", role: "" },
          { id: "rosneft", name: "Роснефть", role: "" },
          { id: "mosvodokanal", name: "МосВодоКанал", role: "" },
        ],
      },
    ],
  },
  {
    id: "okved_10",
    name: "10 — Пищевая промышленность",
    companies: [
      {
        id: "7712_bakery",
        name: "ООО Хлеб&Ко",
        staff: [
          { id: "stf_5", name: "Смирнов В.В.", role: "Директор" },
          { id: "stf_6", name: "Лебедева М.М.", role: "Технолог" },
        ],
      },
    ],
  },
  {
    id: "okved_62",
    name: "62 — Разработка ПО",
    companies: [
      {
        id: "7705_soft",
        name: "ООО СофтЛаб",
        staff: [
          { id: "stf_7", name: "Ковалев Д.Д.", role: "CEO" },
          { id: "stf_8", name: "Орлова Е.Е.", role: "CTO" },
        ],
      },
    ],
  },
];

export default function IndustryForceGraph() {
  const chartRef = useRef<ReactECharts>(null);

  const [expandedSectors, setExpandedSectors] = useState<Set<string>>(
    () => new Set()
  );
  const [expandedCompanies, setExpandedCompanies] = useState<Set<string>>(
    () => new Set()
  );
  const [highlightNodeId, setHighlightNodeId] = useState<string | null>(null);

  /** Построение графа */
  const { nodes, links } = useMemo(() => {
    const n: Array<{ id: string; name: string; category: "root"|"sector"|"company"|"staff"; symbolSize?: number }> = [];
    const l: Array<{ source: string; target: string }> = [];

    n.push({ id: "moscow", name: "Москва", category: "root", symbolSize: 90 });

    for (const sector of SECTORS) {
      n.push({ id: sector.id, name: sector.name, category: "sector", symbolSize: 65 });
      l.push({ source: "moscow", target: sector.id });

      if (expandedSectors.has(sector.id)) {
        for (const comp of sector.companies) {
          n.push({ id: comp.id, name: comp.name, category: "company", symbolSize: 70 });
          l.push({ source: sector.id, target: comp.id });

          if (expandedCompanies.has(comp.id)) {
            for (const stf of comp.staff) {
              n.push({
                id: stf.id,
                name: `${stf.name} ${stf.role}`,
                category: "staff",
                symbolSize: 60,
              });
              l.push({ source: comp.id, target: stf.id });
            }
          }
        }
      }
    }

    if (highlightNodeId) {
      const idx = n.findIndex((x) => x.id === highlightNodeId);
      if (idx >= 0)
        n[idx] = { ...n[idx], symbolSize: Math.max(n[idx].symbolSize ?? 42, 85) };
    }

    return { nodes: n, links: l };
  }, [expandedSectors, expandedCompanies, highlightNodeId]);

  const categories = [
    { name: "Город", color: "#111827" },
    { name: "ОКВЭД", color: "#2563EB" },
    { name: "Компания", color: "#ffee00ff" },
    { name: "Консорциум", color: "#F59E0B" },
  ];

  /** Опции ECharts */
  const option = useMemo(() => {
    return {
      tooltip: {
        formatter: (p: any) =>
          p.dataType === "node"
            ? p.data.name
            : `${p.data.source} → ${p.data.target}`,
      },
      legend: [{ data: categories.map((c) => c.name) }],
      series: [
        {
          type: "graph",
          layout: "force",
          roam: true,
          draggable: true,
          animationDuration: 100,
          animationEasing: "quadraticOut",
          categories: categories.map((c) => ({ name: c.name })),
          label: {
            show: true,
            position: "right",
            fontSize: 12,
            formatter: (p: any) => p.data.name,
          },
          force: {
            repulsion: 2200,
            edgeLength: [90, 200],
            gravity: 0.15,
            friction: 0.2,
          },
          data: nodes.map((node) => {
            const catIndex =
              node.category === "root"
                ? 0
                : node.category === "sector"
                ? 1
                : node.category === "company"
                ? 2
                : 3;

            const isNTC = node.name.includes("НТЦ Приводная техника");

            const color = isNTC
              ? "#DC2626" // 🔴 красный для НТЦ
              : categories[catIndex].color;

            return {
              id: node.id,
              name: node.name,
              category: catIndex,
              symbolSize: node.symbolSize ?? 42,
              itemStyle: {
                color,
                borderColor: "#fff",
                borderWidth: 2,
                shadowBlur: highlightNodeId === node.id ? 25 : 8,
                shadowColor:
                  highlightNodeId === node.id
                    ? "rgba(99,102,241,.7)"
                    : "rgba(0,0,0,.15)",
              },
            };
          }),
          edges: links,
          emphasis: {
            focus: "adjacency",
            lineStyle: { width: 5 },
          },
          lineStyle: {
            curveness: 0.1,
            width: 2,
            color: "rgba(99,102,241,.6)",
          },
        },
      ],
    };
  }, [nodes, links, highlightNodeId]);

  /** Обработчик кликов */
  const onChartEvents = {
    click: (params: any) => {
      if (params?.dataType !== "node") return;
      const id = params.data.id as string;

      const sector = SECTORS.find((s) => s.id === id);
      if (sector) {
        setExpandedSectors((prev) => {
          const next = new Set(prev);
          next.has(id) ? next.delete(id) : next.add(id);
          return next;
        });
        return;
      }

      for (const s of SECTORS) {
        const comp = s.companies.find((c) => c.id === id);
        if (comp) {
          setExpandedCompanies((prev) => {
            const next = new Set(prev);
            next.has(id) ? next.delete(id) : next.add(id);
            return next;
          });
          return;
        }
      }

      if (id === "moscow") {
        setExpandedSectors(new Set());
        setExpandedCompanies(new Set());
        setHighlightNodeId(null);
      }
    },
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <div className="flex justify-between items-center bg-white shadow px-6 py-4">
        <h1 className="text-2xl font-bold text-gray-800">
          Отраслевой граф (Москва → ОКВЭД → Компании → Руководство)
        </h1>
        <Button
          color="gray"
          onClick={() => {
            setExpandedSectors(new Set());
            setExpandedCompanies(new Set());
          }}
        >
          Свернуть всё
        </Button>
      </div>

      <div className="p-4">
        <Card className="shadow-md">
          <div className="h-[72vh]">
            <ReactECharts
              ref={chartRef}
              option={option}
              onEvents={onChartEvents}
              style={{ height: "100%", width: "100%" }}
              notMerge={false}
              lazyUpdate={true}
            />
          </div>
        </Card>
      </div>
    </div>
  );
}
