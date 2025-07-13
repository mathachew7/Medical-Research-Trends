'use client';

import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { fetchFromAPI } from '@/lib/api';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function ForecastChart() {
  const [years, setYears] = useState<string[]>([]);
  const [counts, setCounts] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFromAPI('/forecast')
      .then((res) => {
        if (!res || !Array.isArray(res.years) || !Array.isArray(res.counts)) {
          throw new Error('Invalid response format');
        }
        setYears(res.years);
        setCounts(res.counts);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to fetch forecast:', err);
        setError('Failed to load forecast data');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="bg-gray-800 p-4 rounded-xl shadow text-white w-full min-h-[150px] max-h-[280px] flex items-center justify-center">
        <p className="text-gray-400">Loading forecast data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gray-800 p-4 rounded-xl shadow text-white w-full min-h-[150px] max-h-[280px] flex items-center justify-center">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (!years.length || !counts.length) {
    return (
      <div className="bg-gray-800 p-4 rounded-xl shadow text-white w-full min-h-[150px] max-h-[280px] flex items-center justify-center">
        <p className="text-gray-400">No forecast data available</p>
      </div>
    );
  }

  const currentYear = new Date().getFullYear();

  // Determine color per bar: lighter for published years, darker for predicted
  const backgroundColors = years.map((year) =>
    parseInt(year) <= currentYear ? '#60A5FA' : '#1E40AF'
  );

  const data = {
    labels: years,
    datasets: [
      {
        label: 'Publications',
        data: counts,
        backgroundColor: backgroundColors,
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const idx = context.dataIndex;
            const year = years[idx];
            const value = context.parsed.y ?? context.parsed;
            const status = parseInt(year) <= currentYear ? 'Published' : 'Predicted';
            return `${status}: ${value.toLocaleString()}`;
          },
        },
      },
    },
    scales: {
      x: {
        ticks: { color: '#94A3B8' },
        grid: { display: false },
        barPercentage: 0.6,
        categoryPercentage: 0.6,
        title: {
          display: true,
          text: 'Year',
          color: '#E2E8F0',
        },
      },
      y: {
        ticks: { color: '#94A3B8' },
        grid: { display: false },
        beginAtZero: true,
        title: {
          display: true,
          text: 'Publications',
          color: '#E2E8F0',
        },
      },
    },
  };

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow text-white w-full min-h-[150px] max-h-[280px] flex flex-col">
      <h3 className="text-lg font-semibold mb-4">Forecasted Trends</h3>
      <div className="flex-grow">
        <Bar data={data} options={options} height={null} width={null} />
      </div>
    </div>
  );
}
