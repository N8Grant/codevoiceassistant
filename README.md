# CodeVoiceAssistant

CodeVoiceAssistant is a voice-activated tool to quickly generate high-quality prompts for large language models. It listens for a trigger phrase, transcribes your speech using a local Whisper model, optionally refines the text using OpenAI, and copies the result to your clipboard. It includes a non-intrusive UI overlay and confirmation popup.

---

## Features

- Trigger phrase activation (e.g. "start listening")
- Local speech-to-text using [FasterWhisper](https://github.com/guillaumekln/faster-whisper)
- Real-time visual overlay with live transcript
- Optional LLM refinement via OpenAI
- End command or "Done" button to stop recording
- Automatically copies text to clipboard
- Confirmation window with raw + refined prompt

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/codevoiceassistant.git
cd codevoiceassistant
```

### 2. Install the project
```bash
pip install .
```

### 3.  Create a .env file
```env
# Speech-to-text settings
STT_BACKEND=whisper
WHISPER_MODEL=base.en  # Options: tiny.en, base.en, small.en, medium.en, etc.

# Trigger phrases
TRIGGER_PHRASE=start listening
END_PHRASE=end prompt

# LLM settings
ENABLE_LLM_REFINEMENT=True
OPENAI_API_KEY=your-api-key-here
LLM_PROVIDER=openai
```

---

## Model Size Guide

| Model     | Size (MB) | Speed    | Accuracy  |
| --------- | --------- | -------- | --------- |
| tiny.en   | \~75      | Fast     | Low       |
| base.en   | \~142     | Fast     | Medium    |
| small.en  | \~462     | Moderate | Good      |
| medium.en | \~1.5 GB  | Slower   | Very Good |
| large-v3  | \~2.9 GB  | Slowest  | Best      |

Set your model in .env via WHISPER_MODEL.

---

## Usage
Run from terminal:

```bash
codevoice
```

Speak the trigger phrase (e.g. "start listening") and begin speaking your prompt. When done, either:
- Say the end phrase (e.g. "end prompt"), or
- Click the ✅ Done button on the overlay

Your spoken text will be transcribed, optionally refined by an LLM, and copied to your clipboard. A popup will show the result.

---

## CLI Options
```bash
codevoice <--no-llm>
```

---

## Example Workflow
1. You say: start listening

2. Speak: write a python script to download files from a url list

3. You say: end prompt

4. Prompt is transcribed and refined:
    * Refined: "Write a Python script that reads a list of URLs from a text file and downloads each file using requests."

5. Prompt is copied to clipboard and displayed in a confirmation window.

---

## License
MIT License

---

## Credits
* [FasterWhisper](https://github.com/guillaumekln/faster-whisper)
* [OpenAI Python SDK](https://github.com/openai/openai-python)
* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [Pyperclip](https://github.com/asweigart/pyperclip)
