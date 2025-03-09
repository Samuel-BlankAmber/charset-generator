import os
from random import choices
import sqlite3
import sys
from flask import Flask, request, render_template_string

FLAG_CHARSET = "".join(chr(i) for i in range(33, 127))  # ! to ~

app = Flask(__name__)


def setup_db():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    INSERT INTO users (name, password) VALUES
    ('Samuel', 'mypassword'),
    ('Admin', ?)
    """, (FLAG,))

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return "Welcome to the example CTF challenge! <a href='/login'>Login</a>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("example.db")
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT * FROM users WHERE name = '{username}' AND password = '{password}'")
        user = cursor.fetchone()
        conn.close()

        if user:
            return "Logged in!"

        return "Invalid username or password!", 401

    return render_template_string("""
    <form method="post">
      <input type="text" name="username" placeholder="Username" required>
      <input type="password" name="password" placeholder="Password" required>
      <button type="submit">Login</button>
    </form>
    """)


def gen_flag():
    while True:
        flag = "".join(choices(FLAG_CHARSET, k=38))
        if "'" not in flag:  # Avoid crashing the SQL query
            return flag


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <is-random-flag>")
        sys.exit(1)

    is_random_flag = sys.argv[1].lower() == "true"
    if is_random_flag:
        FLAG = gen_flag()
    else:
        FLAG = "flag{Th1s_1s_my_s3cr3t_3x4mpl3_fl4g!?}"
    assert len(FLAG) == 38
    assert all(c in FLAG_CHARSET for c in FLAG)
    print("Flag:", FLAG)

    setup_db()
    try:
        app.run()
    finally:
        os.remove("example.db")
