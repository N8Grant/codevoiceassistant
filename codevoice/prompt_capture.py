import sys
import json
import subprocess
import tempfile
from pathlib import Path
from PyQt5.QtCore import QTimer, QObject
from codevoice.overlay import ListeningOverlayWidget
from codevoice.notifier import play_start_sound, play_done_sound


class PromptSession(QObject):
    def __init__(self, on_complete):
        super().__init__()
        self.on_complete = on_complete
        self.overlay = ListeningOverlayWidget()
        # self.overlay.set_transcript("")
        self.overlay.done_signal.connect(self._on_manual_done)
        self.proc = None
        self.temp_path = Path(tempfile.gettempdir()) / "codevoice_prompt.json"
        self._finished = False

    def start(self):
        print("[session] Waiting for trigger in subprocess.")
        self._clear_temp_file()
        self._start_listener_process()
        self._poll_trigger_detected()

    def _clear_temp_file(self):
        if self.temp_path.exists():
            self.temp_path.unlink()

    def _start_listener_process(self):
        self.proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "codevoice.audio_listener_process",
                str(self.temp_path),
            ]
        )

    def _poll_trigger_detected(self):
        trigger_flag = self.temp_path.with_name("trigger.txt")

        if trigger_flag.exists():
            print("[session] Trigger detected — showing overlay.")
            trigger_flag.unlink()  # Clean up
            QTimer.singleShot(0, self._start_overlay_and_poll_transcript)
        else:
            QTimer.singleShot(300, self._poll_trigger_detected)

    def _start_overlay_and_poll_transcript(self):
        play_start_sound()
        self.overlay.show()
        self._poll_for_final_result()

    def _poll_for_final_result(self):
        if self.temp_path.exists():
            try:
                result = json.loads(self.temp_path.read_text())
                print("[session] Got final result.")
                self._finalize(result["spoken"])
            except Exception as e:
                print(f"[session] Error reading result: {e}")
                QTimer.singleShot(300, self._poll_for_final_result)
        else:
            QTimer.singleShot(300, self._poll_for_final_result)

    def _on_manual_done(self):
        print("[session] Done button clicked. Waiting for result...")

        exit_flag = self.temp_path.with_name("exit_now.txt")
        exit_flag.write_text("1")

        # Keep trying until file exists or timeout
        self.poll_attempts = 0

        def try_read():
            self.poll_attempts += 1

            if self.temp_path.exists():
                try:
                    result = json.loads(self.temp_path.read_text())
                    prompt = result.get("spoken", "").strip()
                    print(f"[session] Prompt read from file: {prompt!r}")
                    self._finalize(prompt)
                except Exception as e:
                    print(f"[session] Error reading prompt file: {e}")
                    self._finalize("")
            elif self.poll_attempts > 20:  # ~6 seconds max wait
                print("[session] Timed out waiting for result file.")
                self._finalize("")
            else:
                QTimer.singleShot(300, try_read)

        QTimer.singleShot(300, try_read)

    def _finalize(self, text: str):
        """Finish the session exactly once, clean up, and hand the prompt back."""
        if getattr(self, "_finished", False):
            return  # 🔒 Already handled
        self._finished = True

        # ── Step 1: stop audio subprocess ──────────────────────────────
        if hasattr(self, "proc") and self.proc and self.proc.poll() is None:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=1)
                print("[session] Listener subprocess terminated.")
            except Exception as e:
                print(f"[session] Error terminating subprocess: {e}")

        # ── Step 2: stop any repeating timers we created ───────────────
        # (only needed if you stored QTimer objects; shown here for completeness)
        if hasattr(self, "poll_timer") and self.poll_timer:
            self.poll_timer.stop()

        # ── Step 3: overlay & sound  ───────────────────────────────────
        try:
            play_done_sound()
        except Exception:
            pass  # ignore audio errors

        if getattr(self, "overlay", None):
            self.overlay.close()

        # ── Step 4: load prompt from disk (fallback to `text`) ─────────
        prompt = text.strip()
        try:
            if self.temp_path.exists():
                data = json.loads(self.temp_path.read_text())
                prompt = data.get("spoken", prompt).strip()
        except Exception as e:
            print(f"[session] Error reading prompt file: {e}")

        print(f"[session] Final prompt: {prompt!r}")
        self.on_complete(prompt)
