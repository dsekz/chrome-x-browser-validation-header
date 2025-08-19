
# Chrome X-Browser-Validation Header Reverse Engineering & Generator

Chrome recently added a few new headers:
```
"x-browser-channel": "stable",
"x-browser-copyright": "Copyright 2025 Google LLC. All rights reserved.",
"x-browser-validation": "6h3XF8YcD8syi2FF2BbuE2KllQo=",
"x-browser-year": "2025"
```
Apart from one of them, there isn’t much that’s interesting. They’re just bits of client specific information. However, base64 decoding x-browser-validation yields what appears to be a hash whose purpose remains undocumented.

Chrome almost certainly uses this header as an integrity signal. Verifying that the declared user agent matches the underlying platform, spotting user agent string spoofing attempts etc.

---

## Generator

```python
from xbv import generate_validation_header


ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

# You may supply an explicit api_key alongside the ua
# if omitted, the function automatically selects the appropriate key based on the user agent
api_key = "AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE"

header_value = generate_validation_header(ua)

print(header_value)
```

---

## How the Header Is Made

1. **Grab two strings**

   * A hard-coded, platform specific API key
   * The browser’s full user agent string

2. **Concatenate**

   ```
   DATA = API_KEY + USER_AGENT
   ```

3. **Hash** `DATA` with SHA-1 and base64 encode it.

---

## Platform API Keys

| Platform | Default Key (found in Chrome binaries)    |
| -------- | ----------------------------------------- |
| Windows  | `AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE` |
| Linux    | `AIzaSyDlUur5xXJ0gBeLFW_D2PtjduqOFQMsqEY` |
| macOS    | `AIzaSyDr2UxVnv_U85AbhhY8XSHSIavUW0DC-sY` |

---

## Reverse-Engineering


 Opened `chrome.dll` in IDA. The master routine `sub_1806C95B0` builds every `X-Browser-*` header (you can find this function by searching `browser-validation` etc):

- Data prep - grabs the first hard-coded API key for the OS and appends the full user agent.

  ```c
  __int64 __fastcall sub_1806C95B0(__int64 a1, __int64 a2)
  {
      // ... setup ...
  
      // Data Preparation
      // Retrieves credentials and combines the API key and user agent into a buffer.
      v7 = sub_1806C9B30();
      v9 = sub_183EBC7D0(v41, 0LL, v7, v8);
  
      // ... more setup ...
  
      // Hashing
      // The call to the SHA-1 hashing function.
      sub_183B509D0(v46, v38);
  
      // ... more setup ...
      
      // Encoding
      // The call to the Base64 encoding function.
      sub_1806C9A80((__int64 *)v40, v39);
  
      // ... more setup ...
  
      // Header Setting
      // Adds the final encoded string to the request headers.
      v30 = "X-Browser-Validation";
      sub_183C6B920(v27);
      
      // ...
  }
  ```

- Hash - passes that buffer into `sub_183B509D0`, which is SHA-1 algo. Open this guy and the first assignment jumps out:

  ```c
  v12[0] = xmmword_7FFE2C9A7D50;
  LODWORD(v12[1]) = -1009589776;   // 0xC3D2E1F0
  ```

  The second you see that "-1009589776" number, you can literally smell SHA-1.

- Base64 - the 20-byte digest is encoded.

Dynamic confirmation: pause one instruction before the hash call, dump RDX, and the \~150-byte buffer is nothing but

```
<API_KEY><User-Agent>
```

Base64(SHA-1(buffer)) = header. Mystery solved.
