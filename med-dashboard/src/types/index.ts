// src/types/index.ts

export interface StatData {
  total_publications: string;
  top_category: string;
  category_growth_rate: string;
  fastest_growing_category: string;
}

export interface TrendRecord {
  Year: number;
  [category: string]: number | string;
}

export interface KeywordEntry {
  term: string;
  count: number;
  sparkline?: number[];
  category?: string;
  references?: {
    PMID: string;
    Year: number;
    link: string;
  }[];
}

export interface CategoryDistributionEntry {
  category: string;
  count: number;
}

export interface ForecastData {
  years: string[];
  counts: number[];
}
