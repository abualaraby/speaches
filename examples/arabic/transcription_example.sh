#!/usr/bin/env bash

# Arabic Speech-to-Text Example
# This script demonstrates how to use the Speaches API for Arabic transcription

set -e

echo "=== Arabic Speech-to-Text Example ==="
echo

# Configuration
export SPEACHES_BASE_URL="${SPEACHES_BASE_URL:-http://localhost:8000}"
export TRANSCRIPTION_MODEL="${TRANSCRIPTION_MODEL:-Systran/faster-whisper-large-v3}"

# Note: Replace with your Arabic audio file
AUDIO_FILE="${AUDIO_FILE:-audio.wav}"

echo "Configuration:"
echo "  Base URL: $SPEACHES_BASE_URL" 
echo "  Model: $TRANSCRIPTION_MODEL"
echo "  Audio File: $AUDIO_FILE"
echo

# Check if the API server is running
echo "Checking if Speaches server is running..."
if ! curl -s "$SPEACHES_BASE_URL/health" > /dev/null; then
    echo "❌ Error: Speaches server is not running at $SPEACHES_BASE_URL"
    echo "Please start the server first using Docker or directly."
    exit 1
fi
echo "✅ Server is running"
echo

# Check if audio file exists
if [ ! -f "$AUDIO_FILE" ]; then
    echo "❌ Error: Audio file '$AUDIO_FILE' not found!"
    echo "Please provide an Arabic audio file or set the AUDIO_FILE environment variable."
    exit 1
fi
echo "✅ Audio file found: $AUDIO_FILE"
echo

# Example 1: Basic Arabic transcription
echo "=== Example 1: Basic Arabic Transcription ==="
echo "Transcribing with explicit Arabic language setting..."
curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" \
    -F "file=@$AUDIO_FILE" \
    -F "model=$TRANSCRIPTION_MODEL" \
    -F "language=ar" \
    -F "response_format=text" \
    | tee arabic_transcription.txt

echo
echo "✅ Result saved to: arabic_transcription.txt"
echo

# Example 2: Detailed Arabic transcription with JSON output
echo "=== Example 2: Detailed Arabic Transcription (JSON) ==="
echo "Getting detailed transcription with timing information..."
curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" \
    -F "file=@$AUDIO_FILE" \
    -F "model=$TRANSCRIPTION_MODEL" \
    -F "language=ar" \
    -F "response_format=verbose_json" \
    | tee arabic_transcription_detailed.json

echo
echo "✅ Result saved to: arabic_transcription_detailed.json"
echo

# Example 3: Auto language detection vs explicit Arabic
echo "=== Example 3: Language Detection Comparison ==="
echo "Comparing auto-detection vs explicit Arabic setting..."

echo "Auto-detection result:"
AUTO_RESULT=$(curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" \
    -F "file=@$AUDIO_FILE" \
    -F "model=$TRANSCRIPTION_MODEL" \
    -F "response_format=verbose_json")

echo "$AUTO_RESULT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'  Detected language: {data.get(\"language\", \"unknown\")}')
    print(f'  Text: {data.get(\"text\", \"\")}')
except Exception as e:
    print(f'  Error parsing result: {e}')
" 2>/dev/null || echo "  Failed to parse auto-detection result"

echo
echo "Explicit Arabic result:"
echo "$(<arabic_transcription_detailed.json)" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'  Language: {data.get(\"language\", \"unknown\")}')
    print(f'  Text: {data.get(\"text\", \"\")}')
except Exception as e:
    print(f'  Error parsing result: {e}')
" 2>/dev/null || echo "  Failed to parse Arabic result"

echo

# Example 4: Streaming Arabic transcription (if supported)
echo "=== Example 4: Streaming Arabic Transcription ==="
echo "Testing streaming transcription..."
curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" \
    -F "file=@$AUDIO_FILE" \
    -F "model=$TRANSCRIPTION_MODEL" \
    -F "language=ar" \
    -F "response_format=text" \
    -F "stream=true" \
    2>/dev/null || echo "Streaming not available or not supported"

echo
echo

# Summary
echo "=== Summary ==="
echo "✅ Arabic transcription examples completed!"
echo "Generated files:"
echo "  - arabic_transcription.txt (basic text output)"
echo "  - arabic_transcription_detailed.json (detailed JSON with timing)"
echo
echo "Tips for better Arabic transcription:"
echo "  • Use high-quality audio with clear speech"
echo "  • Minimize background noise"
echo "  • Use the Systran/faster-whisper-large-v3 model for best Arabic support"
echo "  • Always specify 'language=ar' when you know the audio is Arabic"
echo "  • Use 'verbose_json' format to get timing and confidence information"
echo