import React, { useState, useEffect } from "react";
import "../styles.css";

export default function SearchBar({ location, setLocation, onSearch }) {
  const [suggestions, setSuggestions] = useState([]);

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      onSearch();
      setSuggestions([]);
    }
  };

  useEffect(() => {
    if (location.length < 2) {
      setSuggestions([]);
      return;
    }

    const controller = new AbortController();

    const fetchSuggestions = async () => {
      try {
        const response = await fetch(
          `https://wft-geo-db.p.rapidapi.com/v1/geo/cities?limit=5&namePrefix=${location}`,
          {
            method: "GET",
            headers: {
              "X-RapidAPI-Key": import.meta.env.VITE_GEODB_KEY,
              "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            },
            signal: controller.signal,
          }
        );
        const data = await response.json();
        const cities = Array.isArray(data.data)
        ? data.data.map(
          (city) => `${city.city}, ${city.region}, ${city.country}`
        )
        : [];
        setSuggestions(cities);
      } catch (error) {
        if (error.name !== "AbortError") {
          console.error("Error fetching suggestions:", error);
        }
      }
    };

    fetchSuggestions();
    return () => controller.abort(); // Cleanup on re-type
  }, [location]);

  const handleSuggestionClick = (suggestion) => {
    setLocation(suggestion);
    setSuggestions([]);
    onSearch();
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Enter a city, region, or country"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        onKeyDown={handleKeyPress}
        className="search-input"
        autoComplete="off"
      />
      <button onClick={onSearch} className="search-button">
        🔍 Search
      </button>
      {suggestions.length > 0 && (
        <ul className="suggestions-list">
          {suggestions.map((s, idx) => (
            <li key={idx} onClick={() => handleSuggestionClick(s)}>
              {s}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
