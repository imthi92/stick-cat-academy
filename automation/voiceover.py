#!/usr/bin/env python3
"""
Stick Cat Academy - Voiceover Generator
Uses EdgeTTS to generate character-specific voiceovers
"""

import asyncio
import os
import edge_tts

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

VOICE_MAP = {
    "professor": "en-US-GuyNeural",
    "luna": "en-US-JennyNeural",
    "mochi": "en-US-ChristopherNeural",
    "owner": "en-US-AriaNeural",
}

DEFAULT_VOICE = "en-US-GuyNeural"

async def generate_line_audio(text, voice, output_path, rate="+0%", pitch="+0Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)

def generate_voiceover_line(text, character, output_path, rate=None, pitch=None):
    voice = VOICE_MAP.get(character, DEFAULT_VOICE)

    if character == "professor":
        rate = rate or "-5%"
        pitch = pitch or "-2Hz"
    elif character == "luna":
        rate = rate or "+5%"
        pitch = pitch or "+3Hz"
    elif character == "mochi":
        rate = rate or "-10%"
        pitch = pitch or "-5Hz"
    elif character == "owner":
        rate = rate or "+0%"
        pitch = pitch or "+0Hz"
    else:
        rate = rate or "+0%"
        pitch = pitch or "+0Hz"

    asyncio.run(generate_line_audio(text, voice, output_path, rate, pitch))
    return output_path

def generate_full_voiceover(script, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    audio_files = []

    lines = script.get("lines", [])
    for i, line in enumerate(lines):
        text = line["text"]
        character = line["character"]
        audio_path = os.path.join(output_dir, f"line_{i:02d}_{character}.mp3")

        print(f"  [TTS] {character}: {text[:40]}...")
        try:
            generate_voiceover_line(text, character, audio_path)
            audio_files.append({
                "path": audio_path,
                "character": character,
                "text": text,
                "line_index": i
            })
            print(f"  [OK] line_{i:02d}_{character}.mp3")
        except Exception as e:
            print(f"  [ERROR] {e}")

    return audio_files

if __name__ == "__main__":
    test_script = {
        "lines": [
            {"character": "professor", "text": "Good morning class! Today we learn about sleep."},
            {"character": "luna", "text": "Oh exciting! I love sleeping!"},
            {"character": "mochi", "text": "Zzz... already practicing..."},
        ]
    }
    output_dir = os.path.join(SCRIPT_DIR, "..", "output", "test_voiceover")
    results = generate_full_voiceover(test_script, output_dir)
    print(f"\nGenerated {len(results)} audio files")
