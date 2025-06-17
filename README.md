# Live Sentient

Live Sentient is a full-stack application for ingesting, enriching, and exploring news articles with advanced NLP techniques. The backend processes a large news dataset, classifies emotion, generates embeddings, and stores enriched records in MongoDB. The frontend provides a modern interface for searching and visualizing news by location, sentiment, and more.

---

## Features

- **Dataset Ingestion**: Reads and processes a large news dataset (`public_dataset/news_category.json`), cleaning and enriching each article.
- **NLP Enrichment**:
  - **Summarization**: Generates concise summaries of articles.
  - **Emotion Classification**: Detects the primary emotion of each article using a transformer model.
  - **Embeddings**: Generates semantic vector embeddings for similarity search and clustering.
- **MongoDB Storage**: Stores enriched articles in a MongoDB Atlas collection.
- **REST API**: Exposes endpoints for querying news, searching by location, and more.
- **Frontend**: React-based UI for searching, filtering, and visualizing news articles.
- **Testing**: Includes unit and integration tests for backend services.

---

## Project Structure

```
Live_Sentient/
│
├── app/                        # Backend application (FastAPI/Flask)
│   ├── config.py
│   ├── main.py
│   ├── db/
│   │   ├── mongo_client.py
│   │   └── schema_setup.py
│   ├── models/
│   │   ├── event.py
│   │   └── user_query.py
│   ├── routes/
│   │   └── query.py
│   ├── services/
│   │   ├── data_ingest.py
│   │   ├── embeddings.py
│   │   └── ...
│   └── utils/
│
├── public_dataset/
│   ├── news_category.json      # Raw news dataset (line-delimited JSON)
│   └── preprocessor.py         # Standalone enrichment script
│
├── frontend/                   # React frontend (Vite)
│   ├── src/
│   │   └── components/
│   │       └── SearchBar.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── tests/                      # Unit and integration tests
│   ├── test_app.py
│   └── test_services_and_utils.py
│
├── .env                        # Environment variables (backend)
├── .env.test                   # Test environment variables
├── README.md
├── run.sh                      # Startup script
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions CI
```

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB Atlas account (or local MongoDB)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
- [Sentence Transformers](https://www.sbert.net/)
- [Vite](https://vitejs.dev/) (for frontend)

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/Live_Sentient.git
cd Live_Sentient
```

### 2. Backend Setup

1. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Configure environment variables:**

    - Copy `.env.example` to `.env` and fill in your MongoDB URI and any other secrets.

4. **Ingest and enrich the dataset:**

    ```sh
    python app/services/data_ingest.py
    ```

    This will process `public_dataset/news_category.json`, enrich each article, and store results in MongoDB.

5. **Run the backend server:**

    ```sh
    python app/main.py
    ```

    The API will be available at `http://localhost:8000` (or as configured).

### 3. Frontend Setup

1. **Install dependencies:**

    ```sh
    cd frontend
    npm install
    ```

2. **Configure environment variables:**

    - Copy `.env.example` to `.env` and set your API endpoints and RapidAPI keys.

3. **Run the frontend:**

    ```sh
    npm run dev
    ```

    The app will be available at `http://localhost:5173` (or as configured).

---

## Usage

- **Search News**: Use the search bar to find news by city, region, or country.
- **Filter by Sentiment/Emotion**: Filter articles by detected emotion or sentiment.
- **Explore Categories**: Browse articles by category (e.g., Politics, Entertainment, Wellness).
- **View Details**: Click on an article to see its summary, emotion, and metadata.

---

## Testing

Run backend tests with:

```sh
pytest tests/
```

---

## Deployment

- Use `run.sh` to automate backend and frontend startup.
- For production, deploy the backend (e.g., with Gunicorn/Uvicorn) and the frontend (e.g., Vercel, Netlify, or static hosting).
- Configure CI/CD with `.github/workflows/ci.yml`.

---

## Environment Variables

- `.env` (backend): `MONGO_URI`, model paths, etc.
- `frontend/.env`: `VITE_GEODB_KEY`, API URLs, etc.

---

## References

- [news_category.json](public_dataset/news_category.json): Source dataset.
- [preprocessor.py](public_dataset/preprocessor.py): Standalone enrichment script.
- [data_ingest.py](app/services/data_ingest.py): Main ingestion and enrichment pipeline.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

- [HuggingFace Transformers](https://huggingface.co/)
- [Sentence Transformers](https://www.sbert.net/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)