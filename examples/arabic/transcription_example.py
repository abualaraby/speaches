#!/usr/bin/env python3
"""
Arabic Speech-to-Text Example

This script demonstrates how to use the Speaches API for Arabic transcription
using both the httpx library and the OpenAI SDK.
"""

import json
from pathlib import Path
import httpx
from openai import OpenAI

# Configuration
SPEACHES_BASE_URL = "http://localhost:8000"
TRANSCRIPTION_MODEL = "Systran/faster-whisper-large-v3"
AUDIO_FILE = "audio.wav"  # Replace with your Arabic audio file


def test_server_connection():
    """Test if the Speaches server is running."""
    try:
        response = httpx.get(f"{SPEACHES_BASE_URL}/health")
        response.raise_for_status()
        print("✅ Server is running")
        return True
    except Exception as e:
        print(f"❌ Error: Server not running - {e}")
        return False


def arabic_transcription_httpx():
    """Example using httpx library for Arabic transcription."""
    print("=== Arabic Transcription with httpx ===")
    
    if not Path(AUDIO_FILE).exists():
        print(f"❌ Error: Audio file '{AUDIO_FILE}' not found!")
        return
    
    # Basic Arabic transcription
    with open(AUDIO_FILE, 'rb') as audio_file:
        files = {'file': (AUDIO_FILE, audio_file, 'audio/wav')}
        data = {
            'model': TRANSCRIPTION_MODEL,
            'language': 'ar',  # Arabic language code
            'response_format': 'text'
        }
        
        response = httpx.post(
            f"{SPEACHES_BASE_URL}/v1/audio/transcriptions", 
            files=files, 
            data=data
        )
        
        if response.status_code == 200:
            transcription = response.text
            print(f"Basic transcription: {transcription}")
            
            # Save to file
            with open('arabic_transcription_httpx.txt', 'w', encoding='utf-8') as f:
                f.write(transcription)
            print("✅ Saved to: arabic_transcription_httpx.txt")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    
    # Detailed Arabic transcription with verbose JSON
    print("\n--- Detailed transcription ---")
    with open(AUDIO_FILE, 'rb') as audio_file:
        files = {'file': (AUDIO_FILE, audio_file, 'audio/wav')}
        data = {
            'model': TRANSCRIPTION_MODEL,
            'language': 'ar',
            'response_format': 'verbose_json'
        }
        
        response = httpx.post(
            f"{SPEACHES_BASE_URL}/v1/audio/transcriptions", 
            files=files, 
            data=data
        )
        
        if response.status_code == 200:
            transcription_data = response.json()
            print(f"Detected language: {transcription_data.get('language', 'unknown')}")
            print(f"Text: {transcription_data.get('text', '')}")
            print(f"Duration: {transcription_data.get('duration', 0):.2f}s")
            
            # Save detailed result
            with open('arabic_transcription_httpx_detailed.json', 'w', encoding='utf-8') as f:
                json.dump(transcription_data, f, ensure_ascii=False, indent=2)
            print("✅ Saved to: arabic_transcription_httpx_detailed.json")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")


def arabic_transcription_openai_sdk():
    """Example using OpenAI SDK for Arabic transcription."""
    print("\n=== Arabic Transcription with OpenAI SDK ===")
    
    if not Path(AUDIO_FILE).exists():
        print(f"❌ Error: Audio file '{AUDIO_FILE}' not found!")
        return
    
    # Initialize OpenAI client with custom base URL
    client = OpenAI(
        base_url=f"{SPEACHES_BASE_URL}/v1",
        api_key="cant-be-empty"  # Required by SDK but not used by Speaches
    )
    
    try:
        # Basic Arabic transcription
        with open(AUDIO_FILE, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=TRANSCRIPTION_MODEL,
                file=audio_file,
                language="ar",  # Arabic language code
                response_format="text"
            )
        
        print(f"Basic transcription: {transcription}")
        
        # Save to file
        with open('arabic_transcription_openai.txt', 'w', encoding='utf-8') as f:
            f.write(transcription)
        print("✅ Saved to: arabic_transcription_openai.txt")
        
        # Detailed transcription with verbose JSON
        print("\n--- Detailed transcription ---")
        with open(AUDIO_FILE, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=TRANSCRIPTION_MODEL,
                file=audio_file,
                language="ar",
                response_format="verbose_json"
            )
        
        print(f"Detected language: {transcription.language}")
        print(f"Text: {transcription.text}")
        print(f"Duration: {transcription.duration:.2f}s")
        
        # Save detailed result
        transcription_dict = transcription.model_dump()
        with open('arabic_transcription_openai_detailed.json', 'w', encoding='utf-8') as f:
            json.dump(transcription_dict, f, ensure_ascii=False, indent=2)
        print("✅ Saved to: arabic_transcription_openai_detailed.json")
        
    except Exception as e:
        print(f"❌ Error with OpenAI SDK: {e}")


def compare_auto_vs_explicit():
    """Compare auto language detection vs explicit Arabic setting."""
    print("\n=== Language Detection Comparison ===")
    
    if not Path(AUDIO_FILE).exists():
        print(f"❌ Error: Audio file '{AUDIO_FILE}' not found!")
        return
    
    client = OpenAI(
        base_url=f"{SPEACHES_BASE_URL}/v1",
        api_key="cant-be-empty"
    )
    
    try:
        # Auto-detection
        with open(AUDIO_FILE, "rb") as audio_file:
            auto_transcription = client.audio.transcriptions.create(
                model=TRANSCRIPTION_MODEL,
                file=audio_file,
                response_format="verbose_json"
            )
        
        print(f"Auto-detected language: {auto_transcription.language}")
        print(f"Auto-detected text: {auto_transcription.text}")
        
        # Explicit Arabic
        with open(AUDIO_FILE, "rb") as audio_file:
            arabic_transcription = client.audio.transcriptions.create(
                model=TRANSCRIPTION_MODEL,
                file=audio_file,
                language="ar",
                response_format="verbose_json"
            )
        
        print(f"Arabic explicit language: {arabic_transcription.language}")
        print(f"Arabic explicit text: {arabic_transcription.text}")
        
    except Exception as e:
        print(f"❌ Error in comparison: {e}")


def main():
    """Main function to run all examples."""
    print("🔊 Arabic Speech-to-Text Examples")
    print("=" * 40)
    print(f"Configuration:")
    print(f"  Base URL: {SPEACHES_BASE_URL}")
    print(f"  Model: {TRANSCRIPTION_MODEL}")
    print(f"  Audio File: {AUDIO_FILE}")
    print()
    
    # Test server connection
    if not test_server_connection():
        print("Please start the Speaches server first.")
        return
    
    # Run examples
    arabic_transcription_httpx()
    arabic_transcription_openai_sdk()
    compare_auto_vs_explicit()
    
    print("\n=== Summary ===")
    print("✅ Arabic transcription examples completed!")
    print("Generated files:")
    print("  - arabic_transcription_httpx.txt")
    print("  - arabic_transcription_httpx_detailed.json")
    print("  - arabic_transcription_openai.txt")
    print("  - arabic_transcription_openai_detailed.json")
    print()
    print("💡 Tips for better Arabic transcription:")
    print("  • Use high-quality audio with clear speech")
    print("  • Minimize background noise")
    print("  • Use multilingual models like Systran/faster-whisper-large-v3")
    print("  • Specify language='ar' when audio is known to be Arabic")


if __name__ == "__main__":
    main()