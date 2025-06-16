import React from "react";
import "../styles.css"; // optional separate styling

const emotionColors = {
  joy: "#28a745",
  fear: "#ffc107",
  anger: "#dc3545",
  sadness: "#6c757d",
  surprise: "#17a2b8",
  disgust: "#8e44ad",
  neutral: "#999999",
};

const emotionEmojis = {
  joy: "😊",
  fear: "😨",
  anger: "😠",
  sadness: "😢",
  surprise: "😲",
  disgust: "🤢",
  neutral: "😐",
};

export default function SentimentCard({ location, mood, insight, timestamp, articles }) {
  const moodColor = emotionColors[mood] || "#444";
  const moodEmoji = emotionEmojis[mood] || "🤖";

  return (
    <div className="sentiment-card">
      <h2>
        {moodEmoji} {location} Update —{" "}
        <span className="timestamp">{new Date(timestamp).toLocaleString()}</span>
      </h2>

      <div className="insight" style={{ borderLeft: `5px solid ${moodColor}` }}>
        <p>{insight}</p>
      </div>

      <h3>📰 Top Headlines</h3>
      <ul className="article-list">
        {articles.map((a, idx) => (
          <li key={idx} className="article-item">
            <a href={a.source} target="_blank" rel="noopener noreferrer">
              <strong>{a.title}</strong>
            </a>
            <p className="summary-text">{a.summary}</p>
            <span className="article-sentiment">Sentiment: <strong>{a.sentiment}</strong></span>
          </li>
        ))}
      </ul>
    </div>
  );
}
