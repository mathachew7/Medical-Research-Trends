'use client';

import { useEffect, useState } from 'react';
import { fetchFromAPI } from '@/lib/api';

type CoOccurrenceTag = {
  term: string;
  count: number;
};

export default function KeywordCoOccurrence() {
  const [tags, setTags] = useState<CoOccurrenceTag[]>([]);

  useEffect(() => {
    fetchFromAPI('/co_occurrence')
      .then((res) => setTags(res || []))
      .catch(() => setTags([]));
  }, []);

  if (!tags.length) {
    return <p className="text-gray-400 text-sm">Loading co-occurrence tags...</p>;
  }

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow text-white w-full">
      <h3 className="text-lg font-semibold mb-4">Keyword Co-occurrence</h3>
      <div className="flex flex-wrap gap-2">
        {tags.map((tag, idx) => (
          <span
            key={idx}
            className="bg-gray-700 text-sm text-white px-3 py-1 rounded-full hover:bg-blue-600 transition"
          >
            {tag.term} ({tag.count})
          </span>
        ))}
      </div>
    </div>
  );
}
