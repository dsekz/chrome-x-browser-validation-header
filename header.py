import requests
import hashlib, base64

data = requests.get(
    "https://raw.githubusercontent.com/elyelysiox/chrome-validation-salt/main/data.json"
).json()

current = data["stable"]["current"]
major = current["version"].split(".")[0]
salt = current["salt"]

# AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE
# AIzaSyAoP6runCgAiXKUSuqLcgr1Hvr3dS8AL78
# AIzaSyBOFRtnLfhvq2x_XyY2lU3ZJFP07i-QFRA

api_key = "AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE"
ua  = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major}.0.0.0 Safari/537.36"

raw = (salt + api_key + ua).encode()
digest = hashlib.sha1(raw).digest()
header = base64.b64encode(digest).decode()

print("header:", header)
print("current:", current)
