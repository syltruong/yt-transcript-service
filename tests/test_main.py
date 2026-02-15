from app.main import _seconds_to_hms, _aggregate_segments, transcript_example
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_seconds_to_hms_basic():
    assert _seconds_to_hms(0) == "00:00:00"
    assert _seconds_to_hms(1) == "00:00:01"
    assert _seconds_to_hms(59) == "00:00:59"
    assert _seconds_to_hms(60) == "00:01:00"
    assert _seconds_to_hms(3661) == "01:01:01"


def test_seconds_to_hms_rounding():
    # rounding to nearest second
    assert _seconds_to_hms(1.4) == "00:00:01"
    assert _seconds_to_hms(1.6) == "00:00:02"


def test_aggregate_segments_empty():
    assert _aggregate_segments([]) == []


def test_aggregate_segments_grouping_and_formatting():
    raw = [
        {"start": 0.0, "duration": 3.0, "text": "alpha"},
        {"start": 3.0, "duration": 4.0, "text": "beta"},
        {"start": 7.0, "duration": 5.0, "text": "gamma"},
        {"start": 12.0, "duration": 2.0, "text": "delta"},
    ]

    out = _aggregate_segments(raw, min_duration=10.0)
    # Expect two groups: first aggregates first three (3+4+5=12), second contains the last (2)
    assert len(out) == 2
    assert out[0]["start"] == "00:00:00"
    assert "alpha" in out[0]["text"] and "gamma" in out[0]["text"]

    assert out[1]["start"] == "00:00:12"


def test_transcript_example_response():
    """Test that /api/v1/transcript_example returns the expected response structure with total_duration_seconds."""
    response = client.get("/api/v1/transcript_example")
    assert response.status_code == 200
    data = response.json()
    
    assert "video_id" in data
    assert "segments" in data
    assert "total_duration" in data
    assert "total_duration_seconds" in data
    assert data["video_id"] == "example"
    assert len(data["segments"]) == 2
    assert data["total_duration"] == "00:00:14"
    assert data["total_duration_seconds"] == 14.0
