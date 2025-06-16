import React, { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import SentimentCard from "./components/SentimentCard";
import HistoryTimeline from "./components/HistoryTimeline";
import { queryLocation } from "./api";
import "./styles.css";

export default function App() {
  const [location, setLocation] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  // Handle theme switch
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  const handleQuery = async () => {
  if (!location.trim()) return;
  setLoading(true);
  setError("");
  setData(null);

  try {
    const result = await queryLocation(location); // <- uses api.js
    setData(result);
  } catch (err) {
    setError(err.message || "Something went wrong.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="app-container">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>🌍 LiveSentient</h1>
        <button onClick={() => setDarkMode(!darkMode)} style={{ marginLeft: "1rem" }}>
          {darkMode ? "☀️ Light" : "🌙 Dark"}
        </button>
      </div>

      <p className="subtitle">Ask: What's the public mood in a place right now?</p>
      <SearchBar location={location} setLocation={setLocation} onSearch={handleQuery} />

      {loading && <p>🔄 Fetching live sentiment...</p>}
      {error && <p className="error">❌ {error}</p>}

      {data && (
        <>
          <SentimentCard
            location={data.location}
            mood={data.dominant_mood}
            insight={data.summary_insight}
            timestamp={data.timestamp}
            articles={data.articles}
          />
          <HistoryTimeline events={data.similar_past || []} />
        </>
      )}
    </div>
  );
}
