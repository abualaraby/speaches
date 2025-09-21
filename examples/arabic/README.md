# Arabic Speech-to-Text Examples

This directory contains examples demonstrating how to use the Speaches API for Arabic language transcription.

## Files

- `transcription_example.sh` - Bash script with comprehensive Arabic transcription examples
- `transcription_example.py` - Python script showing both httpx and OpenAI SDK usage
- `README.md` - This file

## Prerequisites

1. **Speaches server running**: Make sure the Speaches server is running on `http://localhost:8000` (or set `SPEACHES_BASE_URL` environment variable)

2. **Multilingual model**: For best Arabic support, use a multilingual model like:
   - `Systran/faster-whisper-large-v3` (recommended)
   - `Systran/faster-distil-whisper-large-v3`

3. **Arabic audio file**: Have an Arabic audio file ready (replace `audio.wav` with your file or set `AUDIO_FILE` environment variable)

## Usage

### Bash Example

```bash
# Set your audio file
export AUDIO_FILE="path/to/your/arabic_audio.wav"

# Run the example
./transcription_example.sh
```

### Python Example

```bash
# Install dependencies first
pip install httpx openai

# Set your audio file  
export AUDIO_FILE="path/to/your/arabic_audio.wav"

# Run the example
python3 transcription_example.py
```

## Key Features Demonstrated

### Language Support
- Explicit Arabic language specification (`language=ar`)
- Auto language detection vs explicit setting
- Comparison of results

### Response Formats
- Text format for simple transcription
- JSON format for basic structured data
- Verbose JSON format with timing and confidence information

### API Usage Patterns
- Using curl for direct HTTP requests
- Using httpx library for Python HTTP requests
- Using OpenAI SDK for standardized API access

## Arabic Language Code

Use `ar` as the language code for Arabic transcription:

```bash
curl -F "language=ar" ...
```

```python
transcription = client.audio.transcriptions.create(
    language="ar",
    ...
)
```

## Best Practices for Arabic Transcription

1. **Use multilingual models**: Models like `Systran/faster-whisper-large-v3` have better Arabic support than English-only models.

2. **Specify language when known**: If you know the audio is Arabic, always specify `language=ar` for better accuracy.

3. **Audio quality matters**: 
   - Use clear audio with minimal background noise
   - Prefer higher sample rates (16kHz or above)
   - Ensure good microphone quality

4. **Use verbose JSON for debugging**: The `verbose_json` format provides valuable information:
   - Detected language
   - Confidence scores
   - Segment-level timing
   - Word-level timestamps (if supported)

5. **Test with different formats**: Try different response formats to find what works best for your use case.

## Troubleshooting

### Server Not Running
```
❌ Error: Server not running
```
Make sure the Speaches server is started and accessible at the configured URL.

### Model Not Found
```
❌ Error: Model 'model-name' is not installed locally
```
Download the model first using the Speaches CLI or API.

### Audio File Issues
```
❌ Error: Audio file 'file.wav' not found!
```
Ensure the audio file path is correct and the file exists.

### Poor Transcription Quality
- Check audio quality and clarity
- Try with a different/better model
- Ensure the audio is actually in Arabic
- Consider noise reduction preprocessing

## Output Files

The examples generate several output files:

- `arabic_transcription.txt` - Simple text transcription
- `arabic_transcription_detailed.json` - Detailed JSON with timing
- `arabic_transcription_httpx.txt` - Python httpx result
- `arabic_transcription_openai.txt` - OpenAI SDK result
- Various JSON files with detailed transcription data

These files are saved in UTF-8 encoding to properly handle Arabic text.