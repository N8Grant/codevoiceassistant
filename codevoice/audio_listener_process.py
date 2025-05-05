# audio_listener_process.py
import sys
import json
from pathlib import Path
from codevoice.config import (
    TRIGGER_PHRASE,
    END_PHRASE,
    PHASE1_CHUNK_MS,
    PHASE2_CHUNK_MS,
    STT_BACKEND,
)
from rapidfuzz import fuzz

if STT_BACKEND == "whisper":
    from codevoice.listeners.whisper_listener import WhisperListener as VoiceListener
elif STT_BACKEND == "vosk":
    from codevoice.listeners.listener import VoiceListener
else:
    raise ValueError(f"Unknown STT_BACKEND: {STT_BACKEND}")


def main(out_path: str):
    out_path = Path(out_path)
    trigger_flag = out_path.with_name("trigger.txt")
    exit_flag = out_path.with_name("exit_now.txt")
    listener = VoiceListener()

    print(f"[listener] Waiting for trigger: '{TRIGGER_PHRASE}'")

    try:
        # Phase 1: Trigger detection
        while True:
            text = listener.listen_once(chunk_ms=PHASE1_CHUNK_MS).lower().strip()
            print("🗣️", text)
            if fuzz.partial_ratio(TRIGGER_PHRASE.lower(), text) > 85:
                print("✅ Trigger detected.")
                trigger_flag.write_text("1")
                break

        # Phase 2: Prompt capture
        spoken = []
        while True:
            if exit_flag.exists():
                print("[listener] Exit signal received — stopping capture.")
                break

            text = listener.listen_once(chunk_ms=PHASE2_CHUNK_MS).lower().strip()
            print("🗣️", text)
            spoken.append(text)

            if fuzz.partial_ratio(END_PHRASE.lower(), text) > 85:
                print("🛑 End phrase detected.")
                break

        prompt_text = (
            " ".join(spoken).replace(TRIGGER_PHRASE, "").replace(END_PHRASE, "").strip()
        )

        out_path.write_text(json.dumps({"spoken": prompt_text}))
        print(f"[listener] Written to {out_path}")

    finally:
        listener.close()
        if trigger_flag.exists():
            trigger_flag.unlink()
        if exit_flag.exists():
            exit_flag.unlink()


if __name__ == "__main__":
    main(sys.argv[1])
