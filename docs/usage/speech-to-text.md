TODO: add a note about automatic downloads
TODO: mention streaming
TODO: add a demo
TODO: talk about audio format
TODO: add a note about performance
TODO: add a note about vad

!!! note

    Before proceeding, you should be familiar with the [OpenAI Speech-to-Text](https://platform.openai.com/docs/guides/speech-to-text) and the relevant [OpenAI API reference](https://platform.openai.com/docs/api-reference/audio/createTranscription)

## Download a STT model

```bash
export SPEACHES_BASE_URL="http://localhost:8000"

# Listing all available STT models
uvx speaches-cli registry ls --task automatic-speech-recognition | jq '.data | [].id'

# Downloading a Systran/faster-distil-whisper-small.en model
uvx speaches-cli model download Systran/faster-distil-whisper-small.en

# Check that the model has been installed
uvx speaches-cli model ls --task text-to-speech | jq '.data | map(select(.id == "Systran/faster-distil-whisper-small.en"))'
```

## Usage

### Curl

```bash
export SPEACHES_BASE_URL="http://localhost:8000"
export TRANSCRIPTION_MODEL_ID="Systran/faster-distil-whisper-small.en"

# Basic transcription (auto-detect language)
curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" -F "file=@audio.wav" -F "model=$TRANSCRIPTION_MODEL_ID"

# Transcription with specific language (e.g., Arabic)
curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" -F "file=@audio.wav" -F "model=$TRANSCRIPTION_MODEL_ID" -F "language=ar"

# Transcription with verbose JSON response to see detected language
curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" -F "file=@audio.wav" -F "model=$TRANSCRIPTION_MODEL_ID" -F "response_format=verbose_json"
```

### Python

=== "httpx"

    ```python
    import httpx

    with open('audio.wav', 'rb') as f:
        files = {'file': ('audio.wav', f)}
        response = httpx.post('http://localhost:8000/v1/audio/transcriptions', files=files)

    print(response.text)
    ```

### OpenAI SDKs

!!! note

    Although this project doesn't require an API key, all OpenAI SDKs require an API key. Therefore, you will need to set it to a non-empty value. Additionally, you will need to overwrite the base URL to point to your server.

    This can be done by setting the `OPENAI_API_KEY` and `OPENAI_BASE_URL` environment variables or by passing them as arguments to the SDK.

=== "Python"

    ```python
    from pathlib import Path

    from openai import OpenAI

    client = OpenAI()

    with Path("audio.wav").open("rb") as audio_file:
        transcription = client.audio.transcriptions.create(model="Systran/faster-whisper-small", file=audio_file)

    print(transcription.text)
    ```

=== "CLI"

    ```bash
    export OPENAI_BASE_URL=http://localhost:8000/v1/
    export OPENAI_API_KEY="cant-be-empty"
    openai api audio.transcriptions.create -m Systran/faster-whisper-small -f audio.wav --response-format text
    ```

=== "Other"

    See [OpenAI libraries](https://platform.openai.com/docs/libraries).

## Language Support

The speech-to-text functionality supports multiple languages, including Arabic. You can specify the language using the `language` parameter, or let the model auto-detect it.

### Supported Language Codes

Common language codes include:
- `ar` - Arabic (العربية)
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `ru` - Russian
- And many more...

### Arabic Transcription Examples

=== "Curl"

    ```bash
    # Arabic transcription with text output
    curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" \
        -F "file=@arabic_audio.wav" \
        -F "model=Systran/faster-whisper-large-v3" \
        -F "language=ar" \
        -F "response_format=text"

    # Arabic transcription with detailed JSON output
    curl -s "$SPEACHES_BASE_URL/v1/audio/transcriptions" \
        -F "file=@arabic_audio.wav" \
        -F "model=Systran/faster-whisper-large-v3" \
        -F "language=ar" \
        -F "response_format=verbose_json"
    ```

=== "Python"

    ```python
    from openai import OpenAI
    from pathlib import Path

    client = OpenAI(base_url="http://localhost:8000/v1", api_key="cant-be-empty")

    # Arabic transcription
    with Path("arabic_audio.wav").open("rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="Systran/faster-whisper-large-v3",
            file=audio_file,
            language="ar",  # Arabic language code
            response_format="verbose_json"
        )

    print(f"Detected language: {transcription.language}")
    print(f"Transcription: {transcription.text}")
    ```

### Best Practices for Arabic Transcription

1. **Use multilingual models**: For Arabic transcription, use models like `Systran/faster-whisper-large-v3` which support multiple languages including Arabic.

2. **Specify language when known**: If you know the audio is in Arabic, specify `language=ar` for better accuracy.

3. **Audio quality matters**: Ensure clear audio with minimal background noise for best results.

4. **Use verbose JSON**: When testing or debugging, use `response_format=verbose_json` to see the detected language and confidence scores.
