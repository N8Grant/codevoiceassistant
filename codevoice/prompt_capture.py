from codevoice.config import TRIGGER_PHRASE, END_PHRASE, PHASE1_CHUNK_MS, PHASE2_CHUNK_MS, STT_BACKEND
from codevoice.notifier import play_start_sound, play_done_sound
from codevoice.overlay import ListeningOverlay
from rapidfuzz import fuzz

if STT_BACKEND == "whisper":
    from codevoice.listeners.whisper_listener import WhisperListener as VoiceListener
elif STT_BACKEND == "vosk":
    from codevoice.listeners.listener import VoiceListener
else:
    raise ValueError(f"Unknown STT_BACKEND: {STT_BACKEND}")


def capture_prompt():
    listener = VoiceListener()
    overlay = ListeningOverlay()

    try:
        print(f"🎧 Say your trigger phrase: '{TRIGGER_PHRASE}'")

        # Phase 1: Fast trigger detection
        while True:
            text = listener.listen_once(chunk_ms=PHASE1_CHUNK_MS).lower().strip()
            print("🗣️", text)
            if fuzz.partial_ratio(TRIGGER_PHRASE.lower(), text) > 85:
                print("✅ Trigger detected.")
                break

        play_start_sound()
        overlay.show()

        # Phase 2: Slower, high-quality prompt capture
        spoken = []
        while True:
            text = listener.listen_once(chunk_ms=PHASE2_CHUNK_MS).lower().strip()
            print("🗣️", text)
            spoken.append(text)
            overlay.update_transcript(" ".join(spoken))

            if fuzz.partial_ratio(END_PHRASE.lower(), text) > 85 or overlay.manual_end:
                print("🛑 Prompt capture ended.")
                break

        play_done_sound()
        overlay.hide()

        full_text = " ".join(spoken).replace(TRIGGER_PHRASE, "").replace(END_PHRASE, "").strip()
        return full_text

    finally:
        listener.close()
