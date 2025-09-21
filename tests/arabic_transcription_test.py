"""Tests for Arabic language transcription functionality."""

import anyio
from httpx import AsyncClient
import pytest

from speaches.api_types import CreateTranscriptionResponseJson

# Use a multilingual Whisper model that supports Arabic
ARABIC_MODEL_ID = "Systran/faster-whisper-large-v3"
AUDIO_FILE = "audio.wav"


@pytest.mark.asyncio
@pytest.mark.parametrize("pull_model_without_cleanup", [ARABIC_MODEL_ID], indirect=True)
@pytest.mark.usefixtures("pull_model_without_cleanup")
async def test_arabic_transcription_text_format(aclient: AsyncClient) -> None:
    """Test Arabic transcription with text response format."""
    async with await anyio.open_file(AUDIO_FILE, "rb") as f:
        data = await f.read()
    
    kwargs = {
        "files": {"file": ("audio.wav", data, "audio/wav")},
        "data": {
            "model": ARABIC_MODEL_ID,
            "language": "ar",  # Arabic language code
            "response_format": "text",
            "stream": False,
        },
    }
    
    response = await aclient.post("/v1/audio/transcriptions", **kwargs)
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    
    # The response should contain some text (even if the audio isn't actually Arabic)
    transcription = response.text
    assert len(transcription.strip()) > 0
    print(f"Arabic transcription (text): {transcription}")


@pytest.mark.asyncio
@pytest.mark.parametrize("pull_model_without_cleanup", [ARABIC_MODEL_ID], indirect=True)
@pytest.mark.usefixtures("pull_model_without_cleanup")
async def test_arabic_transcription_json_format(aclient: AsyncClient) -> None:
    """Test Arabic transcription with JSON response format."""
    async with await anyio.open_file(AUDIO_FILE, "rb") as f:
        data = await f.read()
    
    kwargs = {
        "files": {"file": ("audio.wav", data, "audio/wav")},
        "data": {
            "model": ARABIC_MODEL_ID,
            "language": "ar",  # Arabic language code
            "response_format": "json",
            "stream": False,
        },
    }
    
    response = await aclient.post("/v1/audio/transcriptions", **kwargs)
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    
    transcription_data = response.json()
    assert "text" in transcription_data
    assert len(transcription_data["text"].strip()) > 0
    print(f"Arabic transcription (json): {transcription_data['text']}")


@pytest.mark.asyncio
@pytest.mark.parametrize("pull_model_without_cleanup", [ARABIC_MODEL_ID], indirect=True)
@pytest.mark.usefixtures("pull_model_without_cleanup")
async def test_arabic_transcription_verbose_json_format(aclient: AsyncClient) -> None:
    """Test Arabic transcription with verbose JSON response format."""
    async with await anyio.open_file(AUDIO_FILE, "rb") as f:
        data = await f.read()
    
    kwargs = {
        "files": {"file": ("audio.wav", data, "audio/wav")},
        "data": {
            "model": ARABIC_MODEL_ID,
            "language": "ar",  # Arabic language code
            "response_format": "verbose_json",
            "stream": False,
        },
    }
    
    response = await aclient.post("/v1/audio/transcriptions", **kwargs)
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    
    transcription_data = response.json()
    assert "text" in transcription_data
    assert "language" in transcription_data
    assert "segments" in transcription_data
    assert len(transcription_data["text"].strip()) > 0
    
    # The detected language should be Arabic when we specify it
    print(f"Detected language: {transcription_data.get('language', 'unknown')}")
    print(f"Arabic transcription (verbose): {transcription_data['text']}")


@pytest.mark.asyncio
@pytest.mark.parametrize("pull_model_without_cleanup", [ARABIC_MODEL_ID], indirect=True)
@pytest.mark.usefixtures("pull_model_without_cleanup")
async def test_auto_language_detection_vs_arabic_explicit(aclient: AsyncClient) -> None:
    """Test comparison between auto-detection and explicit Arabic language setting."""
    async with await anyio.open_file(AUDIO_FILE, "rb") as f:
        data = await f.read()
    
    # Test with auto language detection
    kwargs_auto = {
        "files": {"file": ("audio.wav", data, "audio/wav")},
        "data": {
            "model": ARABIC_MODEL_ID,
            "response_format": "verbose_json",
            "stream": False,
        },
    }
    
    response_auto = await aclient.post("/v1/audio/transcriptions", **kwargs_auto)
    assert response_auto.status_code == 200
    auto_result = response_auto.json()
    
    # Test with explicit Arabic language
    kwargs_arabic = {
        "files": {"file": ("audio.wav", data, "audio/wav")},
        "data": {
            "model": ARABIC_MODEL_ID,
            "language": "ar",
            "response_format": "verbose_json",
            "stream": False,
        },
    }
    
    response_arabic = await aclient.post("/v1/audio/transcriptions", **kwargs_arabic)
    assert response_arabic.status_code == 200
    arabic_result = response_arabic.json()
    
    print(f"Auto-detected language: {auto_result.get('language', 'unknown')}")
    print(f"Auto-detected text: {auto_result['text']}")
    print(f"Arabic explicit text: {arabic_result['text']}")
    
    # Both should produce valid transcriptions
    assert len(auto_result["text"].strip()) > 0
    assert len(arabic_result["text"].strip()) > 0