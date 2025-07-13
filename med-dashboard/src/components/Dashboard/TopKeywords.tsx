'use client';

import { useEffect, useState } from 'react';
import { fetchFromAPI } from '@/lib/api';

export default function TopKeywords() {
  const [keywords, setKeywords] = useState<{ term: string; count: number }[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFromAPI('/stats')
      .then((res) => setKeywords(res.top_keywords || []))
      .catch(() => setError('Failed to load top keywords'));
  }, []);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!keywords.length) return <p className="text-gray-400">Loading keywords...</p>;

  return (
    <div className="bg-gray-800 p-4 rounded-xl text-white shadow w-full">
      <h3 className="text-lg font-semibold mb-3">Top 10 Keywords</h3>
      <ul className="space-y-2">
        {keywords.slice(0, 10).map((kw, i) => (
          <li key={i} className="flex justify-between text-sm border-b border-gray-700 pb-1">
            <span>{kw.term}</span>
            <span className="text-gray-400">{kw.count.toLocaleString()}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
