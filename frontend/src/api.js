const BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

/**
 * Query the LiveSentient backend for real-time sentiment on a location.
 * @param {string} location - City, region, or country.
 * @returns {Promise<object>} - API response with sentiment + past events.
 */
export async function queryLocation(location) {
  const res = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ location,
      timestamp: new Date().toISOString(),

     }),
  });

  if (!res.ok) {
    const { detail } = await res.json();
    throw new Error(detail || "Server error");
  }

  return res.json();
}
