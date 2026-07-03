"""Reviews module — AI reply generator (bot ka dimaag).

Ek review (rating + text) do -> ek achha, chhota, insaan-jaisa reply milega.
Gemini REST API use karta hai (koi bhaari dependency nahi, sirf requests).

Bina Google API ke bhi ye ABHI test ho jata hai -> test_reply.py chalao.
"""
import requests

import config

# tone -> AI ko instruction
_TONES = {
    "friendly":     "warm, friendly aur thoda casual",
    "professional": "polite aur professional",
    "short":        "bahut chhota (ek line), polite",
}

_ENDPOINT = ("https://generativelanguage.googleapis.com/v1beta/models/"
             "{model}:generateContent?key={key}")


def _prompt(rating: int, text: str, business: str, tone: str, language: str, signature: str) -> str:
    tone_desc = _TONES.get(tone, _TONES["friendly"])
    good = rating >= 4
    guide = (
        "Customer khush hai — dil se dhanyavaad do aur dobara aane ko kaho."
        if good else
        "Customer naaraz/nirash hai — pehle sincerely maafi/khed jataao, "
        "cheez ko seriously lene ka bharosa do, aur offline baat karne ko kaho. "
        "Defensive mat bano, bahana mat banao."
    )
    return (
        f"Tum '{business}' business ke owner ki taraf se Google review ka reply likh rahe ho.\n"
        f"Review rating: {rating}/5 star.\n"
        f"Review text: \"{text or '(koi text nahi, sirf rating)'}\"\n\n"
        f"Reply {tone_desc} tone me, {language} language me likho. {guide}\n"
        f"Reply short rakho (1-3 lines), natural insaan jaisa, koi hashtag/emoji spam nahi. "
        f"Customer ka naam mat maano. Sirf reply text do, aur kuch nahi."
        + (f"\nEnd me ye signature add karo: {signature}" if signature else "")
    )


def generate_reply(rating: int, text: str = "", business: str = "our business",
                   tone: str = "friendly", language: str = "English",
                   signature: str = "") -> str:
    """Review ka AI reply lauta do. Key na ho ya API fail ho to ek safe
    fallback reply deta hai (kabhi crash nahi hota)."""
    if not config.GEMINI_API_KEY:
        return _fallback(rating)

    url = _ENDPOINT.format(model=config.GEMINI_MODEL, key=config.GEMINI_API_KEY)
    body = {"contents": [{"parts": [{"text": _prompt(rating, text, business, tone, language, signature)}]}]}
    try:
        r = requests.post(url, json=body, timeout=30)
        r.raise_for_status()
        data = r.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        return reply or _fallback(rating)
    except Exception as e:
        print(f"[ai_reply] Gemini fail ({e}); fallback use kar rahe hain")
        return _fallback(rating)


def _fallback(rating: int) -> str:
    if rating >= 4:
        return "Thank you so much for your kind words — we're so glad you had a great experience! Hope to see you again soon. 🙏"
    return ("We're truly sorry your experience didn't meet expectations. Your feedback matters a lot to us — "
            "please reach out so we can make it right.")
