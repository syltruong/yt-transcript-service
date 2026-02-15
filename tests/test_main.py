from app.main import _seconds_to_hms, _aggregate_segments


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
