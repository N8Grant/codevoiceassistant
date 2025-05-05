# __main__.py

import argparse
import pyperclip
from codevoice.prompt_capture import capture_prompt
from codevoice.llm_refiner import refine_prompt
from codevoice.confirmation import show_confirmation
from codevoice.config import ENABLE_LLM_REFINEMENT

import tkinter as tk
tk.Tk().withdraw()

def main():
    parser = argparse.ArgumentParser(description="🎤 Voice-to-clipboard assistant with optional LLM refinement")
    parser.add_argument(
        "--no-llm", action="store_true",
        help="Skip LLM-based prompt refinement"
    )
    args = parser.parse_args()
    use_llm = ENABLE_LLM_REFINEMENT and not args.no_llm

    print("🚀 CodeVoiceAssistant is now running. Press Ctrl+C to exit.")

    try:
        while True:
            raw_prompt = capture_prompt()

            if use_llm:
                original, refined = refine_prompt(raw_prompt)
                result = refined
            else:
                original = result = raw_prompt
                refined = None

            pyperclip.copy(result)
            show_confirmation(original, refined)

            print("\n📋 Prompt copied to clipboard:")
            print("=" * 60)
            print(result)
            print("=" * 60)
            print("⏳ Waiting for next trigger...\n")

    except KeyboardInterrupt:
        print("\n👋 Exiting CodeVoiceAssistant.")

if __name__ == "__main__":
    main()
