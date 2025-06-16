import React from "react";
import "../styles.css"; // Optional for custom styling

const emotionEmojis = {
  joy: "😊",
  fear: "😨",
  anger: "😠",
  sadness: "😢",
  surprise: "😲",
  disgust: "🤢",
  neutral: "😐",
};

export default function HistoryTimeline({ events }) {
  if (!events || events.length === 0) {
    return (
      <div className="timeline-container">
        <h3>📜 Similar Past Events</h3>
        <p>No emotionally similar past events found for this location.</p>
      </div>
    );
  }

  return (
    <div className="timeline-container">
      <h3>📜 Similar Past Events (Echoes from the Past)</h3>
      <ul className="timeline">
        {events.map((event, index) => (
          <li key={index} className="timeline-event">
            <div className="timestamp">
              {event.timestamp ? new Date(event.timestamp).toLocaleDateString() : "No date"}
            </div>
            <div className="content">
              <span className="emoji">
                {emotionEmojis[event.sentiment] || "🤖"}
              </span>
              <strong>{event.raw_title}</strong>
              <p>{event.summary}</p>
              {event.source_url && (
                <a
                  href={event.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="source-link"
                >
                  🔗 Source
                </a>
              )}
              <p className="emotion">Sentiment: {event.sentiment}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
