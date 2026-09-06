#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from pocket_tts import TTSModel
    import scipy.io.wavfile
except ImportError:
    print("Error: pocket-tts dependencies not installed")
    print("Run: uv sync")
    sys.exit(1)

def run_pocket_tts(folder_name, voice="alba"):
    folder = Path(folder_name)
    script_file = folder / "Script.md"

    # Validate inputs
    if not folder.exists():
        print(f"Error: Folder '{folder_name}' does not exist")
        sys.exit(1)

    if not script_file.exists():
        print(f"Error: {script_file} not found")
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

    print(f"Generating audio from {script_file}...")
    print(f"Text: {text[:50]}..." if len(text) > 50 else f"Text: {text}")
    print("Loading model...")

    try:
        # Load model
        tts_model = TTSModel.load_model()

        # Get voice state using default voice
        voice_state = tts_model.get_state_for_audio_prompt(
            f"hf://kyutai/tts-voices/{voice}-mackenna/casual.wav"
        )

        # Generate audio
        print("Generating speech...")
        audio = tts_model.generate_audio(voice_state, text)

        # Save WAV
        scipy.io.wavfile.write(str(output_wav), tts_model.sample_rate, audio.numpy())
        print(f"✓ Generated WAV: {output_wav}")

    except Exception as e:
        print(f"Error: {e}")
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
        print("Usage: uv run script.py <folder-name> [voice]")
        print("Voices: alba, marius, javert, jean, fantine, cosette, eponine, azelma")
        sys.exit(1)
    folder = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else "alba"
    run_pocket_tts(folder, voice)
