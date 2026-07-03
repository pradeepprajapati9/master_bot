"""Reviews module — Google Business Profile client.

Google se reviews laata hai aur reply post karta hai. Ye tab tak "sota" rehta
hai jab tak Google Business Profile API access + OAuth creds nahi milte (R7).
Structure ready hai — bas creds aane par kaam karne lagega.

Env chahiye (worker se aayenge):
  GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET   (OAuth — access token mint karne ko)

Note: reviews ki read/reply abhi bhi legacy v4 endpoint pe hai
(mybusiness.googleapis.com/v4). Account/location listing naye API pe hai.
"""
import os
import requests

GOOGLE_CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

_V4 = "https://mybusiness.googleapis.com/v4"


def access_token_from_refresh(refresh_token: str) -> str:
    """User ke stored refresh token se ek fresh access token banao."""
    r = requests.post("https://oauth2.googleapis.com/token", timeout=30, data={
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    })
    if r.status_code != 200:
        raise RuntimeError(f"token refresh failed: {r.text[:200]}")
    return r.json()["access_token"]


def list_reviews(access_token: str, account_id: str, location_id: str) -> list:
    """Ek location ke reviews laao. Returns list of review dicts.
    review dict me: reviewId, starRating ('FIVE'..'ONE'), comment, reviewReply?"""
    url = f"{_V4}/accounts/{account_id}/locations/{location_id}/reviews"
    out, page = [], None
    while True:
        params = {"pageSize": 50}
        if page:
            params["pageToken"] = page
        r = requests.get(url, headers={"Authorization": f"Bearer {access_token}"},
                         params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        out.extend(data.get("reviews", []))
        page = data.get("nextPageToken")
        if not page:
            break
    return out


def reply_to_review(access_token: str, account_id: str, location_id: str,
                    review_id: str, text: str) -> None:
    """Ek review pe owner reply post/update karo."""
    url = f"{_V4}/accounts/{account_id}/locations/{location_id}/reviews/{review_id}/reply"
    r = requests.put(url, headers={"Authorization": f"Bearer {access_token}"},
                     json={"comment": text}, timeout=30)
    r.raise_for_status()


# Google 'FIVE'..'ONE' -> int 5..1
_STAR = {"FIVE": 5, "FOUR": 4, "THREE": 3, "TWO": 2, "ONE": 1}
def star_to_int(star: str) -> int:
    return _STAR.get(star, 0)
