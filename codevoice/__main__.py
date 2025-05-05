import argparse
import sys
import pyperclip
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import signal
from codevoice.prompt_capture import PromptSession
from codevoice.confirmation import show_confirmation
from codevoice.llm_refiner import refine_prompt
from codevoice.config import ENABLE_LLM_REFINEMENT

session = None
use_llm = False


def handle_sigint(signum, frame):
    print("\n[main] Ctrl‑C received — shutting down.")

    if session and session.proc and session.proc.poll() is None:
        try:
            session.proc.terminate()
            session.proc.wait(timeout=1)
            print("[main] Listener subprocess terminated.")
        except Exception:
            pass

    # ask Qt to exit its event‑loop
    from PyQt5.QtWidgets import QApplication

    app = QApplication.instance()
    if app:
        app.quit()
    else:
        sys.exit(0)


def run_loop():
    global session

    def on_complete(raw_prompt):
        if use_llm:
            original, refined = refine_prompt(raw_prompt)
            result = refined
        else:
            original = result = raw_prompt
            refined = None

        pyperclip.copy(result)

        # ✅ Run confirmation immediately and block here
        show_confirmation(original, refined)

        # ⏳ After window closes, start again
        QTimer.singleShot(0, run_loop)

    print("[main] Starting new prompt session.")
    session = PromptSession(on_complete)
    session.start()


def main():
    global use_llm

    parser = argparse.ArgumentParser(
        description="🎤 Voice-to-clipboard assistant with optional LLM refinement"
    )
    parser.add_argument(
        "--no-llm", action="store_true", help="Skip LLM-based prompt refinement"
    )
    args = parser.parse_args()
    use_llm = False

    print("🚀 CodeVoiceAssistant is now running. Press Ctrl+C to exit.")

    signal.signal(signal.SIGINT, handle_sigint)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # ✅ Defer until after app is fully ready
    QTimer.singleShot(0, run_loop)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
