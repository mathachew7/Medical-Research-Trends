'use client';

import { useEffect, useState } from 'react';
import { fetchFromAPI } from '@/lib/api';
import type { StatData } from '@/types';

const titles = {
  total_publications: 'Total Publications',
  top_category: 'Top Category',
  category_growth_rate: 'Category Growth Rate',
  fastest_growing_category: 'Fastest Growing Category',
};

export default function StatCard() {
  const [data, setData] = useState<StatData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFromAPI('/stats')
      .then((res) => {
        const mapped: StatData = {
          total_publications: res.total_publications,
          top_category: res.top_category,
          category_growth_rate: res.category_growth ?? res.growth_rate ?? 'N/A',
          fastest_growing_category: res.growth_category ?? 'N/A',
        };
        setData(mapped);
      })
      .catch((err) => {
        console.error('❌ Failed to load stats:', err);
        setError('Failed to load stats');
      });
  }, []);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!data) return <p className="text-gray-400">Loading statistics...</p>;

  const formatValue = (key: string, value: string | number) => {
    if (typeof value === 'number' && key === 'total_publications') {
      return value.toLocaleString();
    }
    return value;
  };

  return (
    <>
      {Object.entries(titles).map(([key, title]) => (
        <div
          key={key}
          className="bg-gray-800 rounded-lg px-6 py-6 text-white shadow-md flex flex-col items-center justify-center min-h-[100px] text-center"
        >
          <p className="text-xs text-gray-400 mb-1 whitespace-nowrap">{title}</p>
          <p className="text-2xl font-bold truncate">
            {formatValue(key, data?.[key as keyof StatData] ?? '')}
          </p>
        </div>
      ))}
    </>
  );
}
