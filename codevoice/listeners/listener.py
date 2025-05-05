# listener.py
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from codevoice.config import MODEL_PATH, SAMPLE_RATE

class VoiceListener:
    def __init__(self, model_path=MODEL_PATH, sample_rate=SAMPLE_RATE):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=sample_rate,
                                  input=True,
                                  frames_per_buffer=8000)
        self.stream.start_stream()

    def listen_once(self):
        """Blocking listen for a single phrase."""
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                return result.get("text", "").strip().lower()

    def listen_until(self, stop_phrases=None):
        stop_phrases = stop_phrases or []
        spoken = []
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip().lower()
                if text:
                    print("🗣️", text)
                    spoken.append(text)
                    if any(stop in text for stop in stop_phrases):
                        break
        return " ".join(spoken)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
