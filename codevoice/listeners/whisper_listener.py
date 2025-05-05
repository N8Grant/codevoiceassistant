
from faster_whisper import WhisperModel
import pyaudio
import numpy as np

class WhisperListener:
    def __init__(self, model_size="base"):
        self.model = WhisperModel(model_size, device='cpu')
        self.chunk_ms = 2000  # Default chunk duration (in ms)
        self.rate = 16000
        self.channels = 1

        self.audio = pyaudio.PyAudio()
        self._open_stream(self.chunk_ms)

    def _open_stream(self, chunk_ms):
        self.chunk_samples = int(self.rate * (chunk_ms / 1000))
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_samples,
        )

    def listen_once(self, chunk_ms: int = None) -> str:
        if chunk_ms:
            # Reconfigure stream if chunk size changed
            if int(self.rate * (chunk_ms / 1000)) != self.chunk_samples:
                self.stream.stop_stream()
                self.stream.close()
                self._open_stream(chunk_ms)

        print("🎙️ Listening...")
        audio_data = self.stream.read(self.chunk_samples)
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        segments, _ = self.model.transcribe(audio_np, language="en", beam_size=5,vad_filter=True)
        return " ".join([segment.text for segment in segments]).strip()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()