# utils.py

import os
import zipfile
import requests
from pathlib import Path
from tqdm import tqdm

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_DIR = Path.home() / ".codevoice" / "models" / "vosk-model-small-en-us-0.15"

def ensure_model_present():
    if MODEL_DIR.exists():
        return str(MODEL_DIR)

    print("📥 Downloading VOSK model...")
    os.makedirs(MODEL_DIR.parent, exist_ok=True)
    zip_path = MODEL_DIR.parent / "model.zip"

    with requests.get(MODEL_URL, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(zip_path, 'wb') as f, tqdm(total=total, unit='B', unit_scale=True) as pbar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))

    print("📦 Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(MODEL_DIR.parent)

    os.remove(zip_path)
    print(f"✅ Model ready at: {MODEL_DIR}")
    return str(MODEL_DIR)
