# **YouTube Transcript Service — FastAPI Specification**

**Purpose:**
Provide a lightweight HTTP API to retrieve YouTube video transcripts (timestamps included) using `youtube-transcript-api`. This service is **stateless** and designed to be called from n8n or any other workflow orchestrator.

---

## **1. General Service Info**

| Field           | Value                                         |
| --------------- | --------------------------------------------- |
| Service Name    | `yt-transcript-service`                  |
| Framework       | FastAPI (Python 3.11+)                        |
| Library         | [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api)                      |
| Deployment      | Docker (optional), can run on VPS             |
| Base URL        | `/api/v1`                                     |
| Authentication  | None for internal use; optional API key later |
| Response Format | JSON                                          |
| Error Handling  | Standard HTTP error codes with JSON body      |

---

## **2. API Endpoints**

### 2.1 `GET /api/v1/transcript`

**Description:**
Fetches the transcript for a given YouTube video ID, returning segments with start time and text.

**Request Parameters (Query)**

| Parameter   | Type         | Required | Description                                     |
| ----------- | ------------ | -------- | ----------------------------------------------- |
| `video_id`  | string       | ✅        | YouTube video ID (e.g., `dQw4w9WgXcQ`)          |
| `languages` | list[string] | ❌        | Preferred languages in order (default `["en"]`) |

**Example Request**

```
GET /api/v1/transcript?video_id=dQw4w9WgXcQ&languages=en,fr
```

**Response**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "segments": [
    {
      "start": 0.0,
      "duration": 4.2,
      "text": "Hello everyone, welcome to the video."
    },
    {
      "start": 4.2,
      "duration": 3.5,
      "text": "Today we will talk about..."
    }
  ]
}
```

**Error Responses**

| Status Code | Meaning                                     | Body Example                                                        |
| ----------- | ------------------------------------------- | ------------------------------------------------------------------- |
| 404         | Transcript not found / unavailable          | `{ "detail": "Transcript not available for video ID dQw4w9WgXcQ" }` |
| 400         | Bad request (missing or invalid `video_id`) | `{ "detail": "video_id query parameter is required" }`              |
| 500         | Internal server error                       | `{ "detail": "Internal server error: <message>" }`                  |

---

### 2.2 Optional `GET /api/v1/health`

**Description:**
Returns service health status. Useful for uptime monitoring.

**Example Response**

```json
{
  "status": "ok",
  "service": "youtube-transcript-service",
  "version": "1.0.0"
}
```

---

## **3. Service Behavior / Requirements**

1. **Stateless**

   * No persistent storage needed.
   * Service can be scaled horizontally.

2. **Error Handling**

   * Return meaningful HTTP error codes.
   * Do not crash on invalid video ID; return 404 instead.

3. **Languages**

   * Attempt requested languages in order.
   * Fallback to auto-generated captions if requested language not available.

4. **Performance**

   * Designed for **short video transcript fetches** (up to 2h videos).
   * Optional caching can be added later.

5. **Deployment Considerations**

   * Optional Docker container:

     * Port: `8000`
     * Base image: `python:3.11-slim`
     * Dependencies: `fastapi`, `uvicorn`, `youtube-transcript-api`
   * Can run behind a reverse proxy if needed.

---

## **4. Example FastAPI Implementation**

```python
from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI(title="YouTube Transcript Service", version="1.0.0")

@app.get("/api/v1/transcript")
def get_transcript(video_id: str = Query(...), languages: list[str] = Query(["en"])):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        return {
            "video_id": video_id,
            "segments": transcript
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "service": "youtube-transcript-service",
        "version": "1.0.0"
    }
```

---

## **5. Future Enhancements (optional)**

1. **Whisper fallback**

   * If no transcript exists, auto-generate using Whisper.

2. **Rate limiting**

   * Protect against abuse / large playlists.

3. **Authentication**

   * API key or JWT for external calls.

4. **Caching**

   * Cache video transcripts for 24–48h to reduce repeated API hits.

5. **Batch fetching**

   * Accept multiple `video_id`s at once for workflow efficiency.
