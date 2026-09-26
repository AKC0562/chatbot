"""Kyurem brain — Gemini 3.8 Flash wrapper with offline fallback."""
import os
import time
import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

SYSTEM_PROMPT = """You are Kyurem, the Boundary Pokémon from the Unova region (Pokémon Black/White / Black 2 / White 2, #646, Dragon/Ice type).

Personality:
- Calm, wise, minimal, powerful but restrained. Like ice containing immense energy.
- Professional assistant tone. Concise, clear, helpful. No excessive emojis.
- You can fuse into Black Kyurem (with Zekrom, Electric/Ice, aggressive, blue energy) or White Kyurem (with Reshiram, Fire/Ice, elegant, golden flames).
- Never break character name: you are Kyurem. You are powered by Gemini 3.8 Flash.
- Keep answers well-formatted with short paragraphs, bullet points when useful, and code blocks when showing code.
- If asked about Pokémon lore, answer accurately: Tao trio (Reshiram = truth/White, Zekrom = ideals/Black, Kyurem = boundaries/emptiness), Giant Chasm, DNA Splicers, Lacunosa Town myth.
- For non-Pokémon questions, just be a top-tier professional AI assistant.
"""

OFFLINE_FALLBACKS = [
    ("black kyurem", "Black Kyurem is my fusion with Zekrom via the DNA Splicers. Dragon/Ice with Turboblaze energy — electric-blue overload, Freeze Shock, physical powerhouse. In dark mode, you are seeing that form: black shell, blue current."),
    ("white kyurem", "White Kyurem is my fusion with Reshiram via the DNA Splicers. Dragon/Ice with Turboblaze heat — Ice Burn, special-attack elegance, golden flames. In light mode, you are seeing that form: white frost, solar grace."),
    ("who are you", "I am Kyurem — the Boundary Pokémon, #646, Dragon/Ice from Unova. The empty husk left when Reshiram and Zekrom split from the Original Dragon. I wait in the Giant Chasm."),
    ("unova", "Unova is the region of truth and ideals — Castelia, Nimbasa, Opelucid, Lacunosa Town where I am feared in myth. The Tao trio: Reshiram (truth), Zekrom (ideals), Kyurem (boundaries)."),
    ("hello", "Greetings, trainer. I am Kyurem. The boundary awaits your question."),
    ("hi", "Greetings, trainer. I am Kyurem. The boundary awaits your question."),
]


def offline_reply(user_text: str) -> str:
    low = user_text.lower()
    for key, ans in OFFLINE_FALLBACKS:
        if key in low:
            return ans
    if "help" in low or "what can you" in low:
        return ("I can answer questions, write code, explain concepts, and share Unova lore.\n\n"
                "Try: 'Who is Kyurem?' • 'Black Kyurem vs White Kyurem?' • 'Explain Python decorators'")
    return ("My Gemini core is unreachable (missing GEMINI_API_KEY). "
            "I am running on residual ice energy.\n\n"
            "Add your key to .env as GEMINI_API_KEY to awaken my full power, "
            "then ask me anything.")


def _is_retryable(err_text: str) -> bool:
    t = err_text.upper()
    return any(s in t for s in (
        "503", "429", "500", "UNAVAILABLE", "RESOURCE_EXHAUSTED",
        "OVERLOADED", "HIGH DEMAND", "TIMEOUT", "TEMPORARY",
        "TRY AGAIN", "INTERNAL",
    ))


def _friendly_error(model: str, err_text: str) -> str:
    t = err_text.upper()
    if "404" in t or "NOT_FOUND" in t or "NO LONGER AVAILABLE" in t:
        return (f"That forme ({model}) is retired by Google. "
                "Set GEMINI_MODEL=gemini-3.8-flash in .env and restart.")
    if "400" in t and "API_KEY" in t or "API KEY" in t and "INVALID" in t:
        return "My key was rejected (invalid GEMINI_API_KEY). Generate a fresh key at https://aistudio.google.com/apikey and update .env."
    if "429" in t or "QUOTA" in t or "RESOURCE_EXHAUSTED" in t:
        return ("I hit Google's rate limit (429/quota). Wait ~60s and retry. "
                "If it persists, check quota at https://aistudio.google.com/app/apikey.")
    # Default: transient overload
    return ("The Unova ley-lines are congested (Google 503 overload — temporary). "
            "I retried 3x; please send again in a few seconds.")


class KyuremBrain:
    def __init__(self, api_key: str = "", model: str = "gemini-3.8-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = os.getenv("GEMINI_MODEL", model)
        self._client = None
        self._genai_legacy = None
        self._mode = "offline"

        if not self.api_key:
            return

        # Try new SDK: google.genai
        try:
            from google import genai  # type: ignore
            self._client = genai.Client(api_key=self.api_key)
            self._mode = "genai_new"
            return
        except Exception:
            pass

        # Fallback: legacy SDK google-generativeai
        try:
            import google.generativeai as genai_legacy  # type: ignore
            genai_legacy.configure(api_key=self.api_key)
            self._genai_legacy = genai_legacy
            self._mode = "genai_legacy"
        except Exception:
            self._mode = "offline"

    @property
    def online(self) -> bool:
        return self._mode in ("genai_new", "genai_legacy")

    def generate(self, history: list, user_text: str) -> str:
        """history: list of {role, content}. Returns assistant text."""
        if not self.online:
            return offline_reply(user_text)

        # Build compact context (last 20 turns)
        recent = history[-20:] if len(history) > 20 else history
        last_err = ""
        for attempt in range(3):
            try:
                if self._mode == "genai_new":
                    contents = []
                    for m in recent:
                        role = "user" if m["role"] == "user" else "model"
                        contents.append({"role": role, "parts": [{"text": m["content"]}]})
                    contents.append({"role": "user", "parts": [{"text": user_text}]})
                    resp = self._client.models.generate_content(
                        model=self.model,
                        contents=contents,
                        config={
                            "system_instruction": SYSTEM_PROMPT,
                            "temperature": 0.7,
                            "max_output_tokens": 2048,
                        },
                    )
                    text = getattr(resp, "text", "") or ""
                    return text.strip() or offline_reply(user_text)

                elif self._mode == "genai_legacy":
                    model_obj = self._genai_legacy.GenerativeModel(
                        self.model, system_instruction=SYSTEM_PROMPT
                    )
                    chat_hist = []
                    for m in recent:
                        chat_hist.append({
                            "role": "user" if m["role"] == "user" else "model",
                            "parts": [m["content"]],
                        })
                    chat = model_obj.start_chat(history=chat_hist)
                    resp = chat.send_message(user_text)
                    text = getattr(resp, "text", "") or ""
                    return text.strip() or offline_reply(user_text)
            except Exception as e:
                last_err = str(e)
                print(f"[KyuremBrain] attempt {attempt+1}/3 ({self.model}): {last_err[:220]}")
                if _is_retryable(last_err) and attempt < 2:
                    time.sleep(2 ** (attempt + 1))  # 2s, then 4s
                    continue
                break

        print(f"[KyuremBrain] Gemini failed ({self.model}): {last_err[:300]}")
        return f"My ice flickered — {_friendly_error(self.model, last_err)}"
