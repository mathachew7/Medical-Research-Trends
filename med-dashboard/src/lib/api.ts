// src/lib/api.ts
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

export async function fetchFromAPI(endpoint: string) {
  try {
    const res = await fetch(`${BASE_URL}${endpoint}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error(`Fetch failed for ${endpoint}:`, err);
    throw err;
  }
}
