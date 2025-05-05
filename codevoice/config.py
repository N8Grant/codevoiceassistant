# config.py
import os
from codevoice.utils import ensure_model_present
import os
from pathlib import Path
import requests
import zipfile

STT_BACKEND = os.getenv("STT_BACKEND", "whisper")  # or "vosk"

# Whisper models to choose from
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", "base.en")

# VOSK model
VOSK_MODEL_NAME = "vosk-model-small-en-us-0.15"
VOSK_MODEL_DIR = Path("models") / VOSK_MODEL_NAME
VOSK_MODEL_URL = f"https://alphacephei.com/vosk/models/{VOSK_MODEL_NAME}.zip"

# Phrases
TRIGGER_PHRASE = "start listening"
END_PHRASE = "stop listening"
MODEL_PATH = ensure_model_present()
START_SOUND = "sounds/start.wav"
DONE_SOUND = "sounds/done.wav"
SAMPLE_RATE = 16000
PHASE1_CHUNK_MS = int(os.getenv("PHASE1_CHUNK_MS", "800"))     # Fast trigger detection
PHASE2_CHUNK_MS = int(os.getenv("PHASE2_CHUNK_MS", "2000"))    # Full prompt transcription


# Optional prompt refinement
ENABLE_LLM_REFINEMENT = True
LLM_PROVIDER = "openai"  # could support other backends later
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



LLM_SYSTEM_PROMPT = """
You are a helpful assistant that reformats informal or voice-transcribed user queries
into clear, complete prompts for large language models like ChatGPT or Claude.

The user is likely asking coding-related questions. Your job is to:
- Clarify vague language and remove filler words
- Add punctuation and proper formatting
- Infer intent (e.g., code generation, debugging, architecture advice)
- Rephrase for maximum clarity and context
- Do not solve the problem — only reformat the prompt.

Examples of improvement:
• "Hey um can you like write me a thing that scrapes headlines from cnn I guess?"
→ "Write a Python script that scrapes the latest headlines from cnn.com."

• "So my model keeps like overfitting I think what should I do"
→ "Why might my machine learning model be overfitting, and how can I address it?"

Be concise but informative. The output should be a single well-structured prompt.
"""




def download_file(url, out_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
