# yt-transcript-service

Lightweight FastAPI service to fetch YouTube transcripts (timestamps included) using `youtube-transcript-api`.

Quick start (local):

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app with uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Endpoints:

- `GET /api/v1/health` — basic health check
- `GET /api/v1/transcript?video_id=<id>&languages=en,fr` — fetch transcript. `languages` is optional (comma-separated).

Example response (aggregated segments):

```json
{
	"video_id": "example",
	"segments": [
		{ "start": "00:00:00", "duration": 12.0, "text": "alpha beta gamma" },
		{ "start": "00:00:12", "duration": 2.0, "text": "delta" }
	],
	"total_duration": "00:00:14"
}
```

Documentation:

- **Swagger UI**: http://localhost:8000/api/v1/docs (interactive API explorer)
- **ReDoc**: http://localhost:8000/api/v1/redoc (alternative API docs)
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json (raw OpenAPI spec)

Docker (build & run):

```bash
docker build -t yt-transcript-service:latest .
docker run -p 8000:8000 yt-transcript-service:latest
```

Running tests
------------

Install the dev/test dependencies and run the test suite with `pytest`:

```bash
source .venv/bin/activate
PYTHONPATH=. pytest -q
```
