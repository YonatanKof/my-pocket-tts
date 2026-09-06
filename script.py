#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def run_pocket_tts(folder_name):
    folder = Path(folder_name)
    script_file = folder / "Script.md"
    voice_file = Path("voice.wav")

    # Validate inputs
    if not folder.exists():
        print(f"Error: Folder '{folder_name}' does not exist")
        sys.exit(1)

    if not script_file.exists():
        print(f"Error: {script_file} not found")
        sys.exit(1)

    if not voice_file.exists():
        print(f"Error: voice.wav not found in current directory")
        sys.exit(1)

    # Read text
    text = script_file.read_text().strip()
    if not text:
        print(f"Error: {script_file} is empty")
        sys.exit(1)

    # Generate output filenames
    date = datetime.now().strftime("%y-%m-%d")
    output_wav = folder / f"{date}-{folder_name}.wav"
    output_mp3 = folder / f"{date}-{folder_name}.mp3"

    # Call pocket-tts generate
    print(f"Generating audio from {script_file}...")
    print(f"Text: {text[:50]}..." if len(text) > 50 else f"Text: {text}")

    cmd = [
        "pocket-tts",
        "generate",
        "--text", text,
        "--voice", str(voice_file),
        "--output-path", str(output_wav)
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✓ Generated WAV: {output_wav}")
    except subprocess.CalledProcessError as e:
        print(f"Error: pocket-tts failed with code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: pocket-tts not found. Install with: pipx install pocket-tts")
        sys.exit(1)

    # Convert WAV to MP3 using ffmpeg
    print("Converting to MP3...")
    convert_cmd = ["ffmpeg", "-i", str(output_wav), "-q:a", "9", "-y", str(output_mp3)]

    try:
        subprocess.run(convert_cmd, check=True, capture_output=True)
        print(f"✓ Generated: {output_mp3}")
        output_wav.unlink()  # Delete temporary WAV file
    except FileNotFoundError:
        print(f"Error: ffmpeg not found. Install with: brew install ffmpeg")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: ffmpeg conversion failed")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder-name>")
        sys.exit(1)
    run_pocket_tts(sys.argv[1])
