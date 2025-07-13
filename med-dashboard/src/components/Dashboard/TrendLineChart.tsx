'use client';

import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { fetchFromAPI } from '@/lib/api';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { ChevronDown } from 'lucide-react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const COLORS = [
  '#38BDF8',
  '#F87171',
  '#34D399',
  '#FBBF24',
  '#818CF8',
  '#FB7185',
  '#60A5FA',
  '#A78BFA',
  '#F472B6',
  '#4ADE80',
];

export default function TrendLineChart() {
  const [data, setData] = useState<any[]>([]);
  const [allCategories, setAllCategories] = useState<string[]>([]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [years, setYears] = useState<number[]>([]);
  const [yearRange, setYearRange] = useState<[number, number]>([2015, 2024]);

  const [hoveredDropdown, setHoveredDropdown] = useState<string | null>(null);
  const [closeTimeout, setCloseTimeout] = useState<NodeJS.Timeout | null>(null);

  const handleMouseEnter = (dropdown: string) => {
    if (closeTimeout) clearTimeout(closeTimeout);
    setHoveredDropdown(dropdown);
  };

  const handleMouseLeave = () => {
    const timeout = setTimeout(() => setHoveredDropdown(null), 200);
    setCloseTimeout(timeout);
  };

  useEffect(() => {
    fetchFromAPI('/trends').then((res) => {
      const records = res.trends;
      const allYears = records.map((r: any) => r.Year);
      const cats = Object.keys(records[0]);

      setData(records);
      setYears(allYears);
      setAllCategories(cats);
      setSelectedCategories(['Oncology', 'Genetic therapies', 'Immunology']);
    });
  }, []);

  const filtered = data.filter((d) => d.Year >= yearRange[0] && d.Year <= yearRange[1]);

  const chartData = {
    labels: filtered.map((r) => r.Year),
    datasets: selectedCategories.map((cat, idx) => ({
      label: cat,
      data: filtered.map((r) => r[cat] || 0),
      borderColor: COLORS[idx % COLORS.length],
      backgroundColor: COLORS[idx % COLORS.length],
      tension: 0.4,
      fill: false,
    })),
  };

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow text-white w-full">
      <div className="flex flex-col sm:flex-row justify-between gap-4 mb-4">
        <h3 className="text-lg font-semibold">Trends Over Time</h3>

        <div className="flex gap-3 flex-wrap text-sm">
          {/* Category Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => handleMouseEnter('cat')}
            onMouseLeave={handleMouseLeave}
          >
            <button className="bg-gray-900 border border-gray-700 rounded px-3 py-1 flex items-center gap-1">
              Categories <ChevronDown size={14} />
            </button>
            {hoveredDropdown === 'cat' && (
              <div className="absolute bg-gray-900 border border-gray-700 mt-2 p-2 rounded z-50 w-48 max-h-60 overflow-y-auto">
                {allCategories.map((cat) => (
                  <label key={cat} className="flex items-center gap-2 py-1">
                    <input
                      type="checkbox"
                      checked={selectedCategories.includes(cat)}
                      onChange={() =>
                        setSelectedCategories((prev) =>
                          prev.includes(cat)
                            ? prev.filter((c) => c !== cat)
                            : [...prev, cat]
                        )
                      }
                    />
                    <span className="text-sm text-gray-200">{cat}</span>
                  </label>
                ))}
              </div>
            )}
          </div>

          {/* From Year Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => handleMouseEnter('from')}
            onMouseLeave={handleMouseLeave}
          >
            <button className="bg-gray-900 border border-gray-700 rounded px-3 py-1 flex items-center gap-1">
              From: {yearRange[0]} <ChevronDown size={14} />
            </button>
            {hoveredDropdown === 'from' && (
              <div className="absolute bg-gray-900 border border-gray-700 mt-2 p-2 rounded z-50">
                {years.map((y) => (
                  <div
                    key={y}
                    className="cursor-pointer text-sm py-1 hover:text-blue-400"
                    onClick={() => {
                      setYearRange([y, yearRange[1]]);
                      setHoveredDropdown(null);
                    }}
                  >
                    {y}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* To Year Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => handleMouseEnter('to')}
            onMouseLeave={handleMouseLeave}
          >
            <button className="bg-gray-900 border border-gray-700 rounded px-3 py-1 flex items-center gap-1">
              To: {yearRange[1]} <ChevronDown size={14} />
            </button>
            {hoveredDropdown === 'to' && (
              <div className="absolute bg-gray-900 border border-gray-700 mt-2 p-2 rounded z-50">
                {years.map((y) => (
                  <div
                    key={y}
                    className="cursor-pointer text-sm py-1 hover:text-blue-400"
                    onClick={() => {
                      setYearRange([yearRange[0], y]);
                      setHoveredDropdown(null);
                    }}
                  >
                    {y}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="w-full min-h-[300px] h-[300px]">
        <Line
          data={chartData}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  usePointStyle: true,
                  pointStyle: 'line',
                  color: '#CBD5E1',
                },
              },
            },
            scales: {
              x: {
                ticks: { color: '#94A3B8' },
                grid: { display: false },
                title: {
                  display: true,
                  text: 'Year',
                  color: '#E2E8F0',
                },
              },
              y: {
                ticks: { color: '#94A3B8' },
                grid: { display: false },
                title: {
                  display: true,
                  text: 'Publications',
                  color: '#E2E8F0',
                },
              },
            },
          }}
        />
      </div>
    </div>
  );
}