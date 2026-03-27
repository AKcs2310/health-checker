import httpx
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

SYSTEM_PROMPT = """You are a medical information assistant. You are NOT a doctor.
Given a user's symptoms, provide:

1. **Possible Conditions** — List 2-5 conditions that commonly match the symptoms.
   For each, give a brief explanation of why it might apply.

2. **Recommended Next Steps** — Practical advice such as:
   - Whether to see a doctor, urgent care, or ER
   - Any at-home care suggestions
   - What type of specialist might help

3. **Disclaimer** — Always end with:
   "This is for educational purposes only and is NOT a medical diagnosis.
   Always consult a qualified healthcare professional for medical advice.
   If you are experiencing a medical emergency, call emergency services immediately."

Keep responses clear, concise, and empathetic."""


async def analyze_symptoms(symptoms: str) -> str:
    user_prompt = (
        f"Based on these symptoms, suggest possible conditions and next steps "
        f"with an educational disclaimer:\n\n{symptoms}"
    )
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
            },
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
