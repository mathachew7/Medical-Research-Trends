'use client';

import { useEffect, useState } from 'react';
import { fetchFromAPI } from '@/lib/api';

interface Abstract {
  title: string;
  Year: number;
  PMID?: string;
}

export default function RecentAbstracts() {
  const [abstracts, setAbstracts] = useState<Abstract[]>([]);

  useEffect(() => {
    fetchFromAPI('/recent_abstracts')
      .then((res) => setAbstracts(res.slice(0, 5))) // limit to 6
      .catch(() => setAbstracts([]));
  }, []);

  if (!abstracts.length) {
    return <p className="text-gray-400 text-sm">Loading recent abstracts...</p>;
  }

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow text-white w-full h-full flex flex-col">
      <h3 className="text-lg font-semibold mb-4 flex-shrink-0">Recent Abstracts</h3>
      <ul className="space-y-3 text-sm overflow-y-auto flex-grow">
        {abstracts.map((item, idx) => (
          <li key={idx} className="border-b border-gray-700 pb-2">
            <p className="text-gray-100 font-medium">{item.title}</p>
            <p className="text-gray-400 text-xs mt-1">
              Year: {item.Year}{' '}
              {item.PMID && (
                <a
                  href={`https://pubmed.ncbi.nlm.nih.gov/${item.PMID}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 ml-2 hover:underline"
                >
                  [PubMed]
                </a>
              )}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
