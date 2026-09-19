## Pocket TTS

Add a subfolder inside `content/` with a `text.md` file and run the script. An MP3 is generated in the same subfolder. The `content/` folder is gitignored so your personal projects stay local.

### Setup

```sh
uv sync
```

### Run

```sh
# Basic (uses default voice: eponine)
uv run script.py content/<folder-name>

# With a specific built-in voice
uv run script.py content/<folder-name> <voice>

# With a custom voice file
uv run script.py content/<folder-name> path/to/voice.wav

# Example
uv run script.py content/my-project azelma
```

### Voices

Built-in: `alba`, `marius`, `javert`, `jean`, `fantine`, `cosette`, **`eponine`** (default), `azelma`

You can also use any `.wav` file as a custom voice prompt.

Check out samples in the [`Voices/`](Voices/) folder.
