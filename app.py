from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
import sqlite3
import bcrypt

app = Flask(**name**)
app.secret_key = "secret123"

socketio = SocketIO(app, cors_allowed_origins="*")

# Database Setup

def init_db():
conn = sqlite3.connect("database.db")
c = conn.cursor()

```
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    message TEXT
)
""")

conn.commit()
conn.close()
```

init_db()

# Home

@app.route("/")
def home():
if "user" not in session:
return redirect("/login")

```
return render_template(
    "chat.html",
    username=session["user"]
)
```

# Register

@app.route("/register", methods=["GET", "POST"])
def register():

```
if request.method == "POST":

    username = request.form["username"]
    password = request.form["password"]

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, hashed)
        )

        conn.commit()

        return redirect("/login")

    except:
        return "User already exists"

return render_template("register.html")
```

# Login

@app.route("/login", methods=["GET", "POST"])
def login():

```
if request.method == "POST":

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    user = c.fetchone()

    if user:

        if bcrypt.checkpw(
            password.encode(),
            user[0]
        ):

            session["user"] = username

            return redirect("/")

    return "Invalid Login"

return render_template("login.html")
```

# Logout

@app.route("/logout")
def logout():

```
session.clear()

return redirect("/login")
```

# Socket Messaging

@socketio.on("send_message")
def handle_message(data):

```
conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute(
    "INSERT INTO messages(sender,message) VALUES(?,?)",
    (
        data["sender"],
        data["message"]
    )
)

conn.commit()
conn.close()

emit(
    "receive_message",
    data,
    broadcast=True
)
```

if **name** == "**main**":

```
socketio.run(
    app,
    host="0.0.0.0",
    port=5000,
    debug=True,
    allow_unsafe_werkzeug=True
)
```
