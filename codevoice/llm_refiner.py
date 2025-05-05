# llm_refiner.py

from openai import OpenAI
from codevoice.config import ENABLE_LLM_REFINEMENT, LLM_SYSTEM_PROMPT, LLM_PROVIDER
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4.1-nano"
client = OpenAI(api_key=api_key) if api_key else None


def refine_prompt(raw_prompt: str) -> tuple[str, str]:
    if not ENABLE_LLM_REFINEMENT:
        return raw_prompt, raw_prompt

    if LLM_PROVIDER != "openai":
        print("[LLM Refiner] Unsupported LLM provider.")
        return raw_prompt, raw_prompt

    if not client:
        print("[LLM Refiner] Missing OpenAI API key.")
        return raw_prompt, raw_prompt

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": LLM_SYSTEM_PROMPT},
                {"role": "user", "content": raw_prompt},
            ],
            temperature=0.5,
        )
        refined = response.choices[0].message.content.strip()
        print("✨ Prompt refined by LLM.")
        return raw_prompt, refined
    except Exception as e:
        print(f"[LLM Refiner] Error calling LLM: {e}")
        return raw_prompt, raw_prompt
