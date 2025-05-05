# notifier.py
import numpy as np
import simpleaudio as sa


def _beep(frequency=440, duration_ms=200, volume=0.3):
    fs = 44100  # Sampling rate
    t = np.linspace(0, duration_ms / 1000, int(fs * duration_ms / 1000), False)
    tone = np.sin(frequency * 2 * np.pi * t)
    audio = (tone * volume * (2**15 - 1)).astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()


def play_start_sound():
    # Ascending two-tone beep
    _beep(600, 100)
    _beep(800, 100)


def play_done_sound():
    # Descending two-tone beep
    _beep(800, 100)
    _beep(600, 100)
