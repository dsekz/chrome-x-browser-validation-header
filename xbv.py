import hashlib
import base64

PLATFORM_API_KEYS = {
    "windows": "AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE",
    "linux":   "AIzaSyDlUur5xXJ0gBeLFW_D2PtjduqOFQMsqEY",
    "macos":   "AIzaSyDr2UxVnv_U85AbhhY8XSHSIavUW0DC-sY",
}

def generate_validation_header(user_agent: str, api_key: str | None = None) -> str:
    if api_key is None:
        ua = user_agent.lower()
        if "windows" in ua:
            api_key = PLATFORM_API_KEYS["windows"]
        elif "linux" in ua:
            api_key = PLATFORM_API_KEYS["linux"]
        elif "macintosh" in ua or "mac os x" in ua:
            api_key = PLATFORM_API_KEYS["macos"]
        else:
            raise ValueError("Unknown OS in user agent. Supply api_key manually.")

    data = (api_key + user_agent).encode()
    digest = hashlib.sha1(data).digest()
    return base64.b64encode(digest).decode()