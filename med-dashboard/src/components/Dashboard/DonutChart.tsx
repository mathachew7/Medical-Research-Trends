'use client';

import { useEffect, useState } from 'react';
import { fetchFromAPI } from '@/lib/api';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function DonutChart() {
  const [categoryData, setCategoryData] = useState<any[]>([]);

  useEffect(() => {
    fetchFromAPI('/category_distribution')
      .then((res) => setCategoryData(res || []))
      .catch(() => setCategoryData([]));
  }, []);

  const colors = [
    '#38BDF8', '#F87171', '#34D399', '#FBBF24', '#818CF8',
    '#FB7185', '#60A5FA', '#A78BFA', '#F472B6', '#4ADE80',
  ];

  const data = {
    labels: categoryData.map((d) => d.category),
    datasets: [
      {
        data: categoryData.map((d) => d.count),
        backgroundColor: colors,
        borderWidth: 0,
      },
    ],
  };

  return (
    <div className="bg-gray-800 rounded-lg shadow text-white w-full h-full flex flex-col justify-between">
      <h3 className="text-base font-semibold px-4 pt-4">Top Categories</h3>
      <div className="flex items-start gap-4 px-4 pb-4">
        <div className="w-1/2">
          <Doughnut
            data={data}
            options={{
              cutout: '60%',
              plugins: { legend: { display: false } },
              maintainAspectRatio: false,
            }}
          />
        </div>
        <div className="w-1/2 space-y-1">
          {categoryData.map((d, idx) => (
            <div key={d.category} className="flex items-center gap-2 text-xs text-gray-300">
              <div
                className="w-3 h-0.5 rounded-full"
                style={{ backgroundColor: colors[idx % colors.length] }}
              />
              <span className="truncate">{d.category}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
