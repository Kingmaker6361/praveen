import streamlit as st
import sqlite3
import os
from datetime import datetime

DB = "chat.db"

conn = sqlite3.connect(DB, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT UNIQUE,
password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS messages(
id INTEGER PRIMARY KEY,
sender TEXT,
message TEXT,
filename TEXT,
timestamp TEXT
)
""")

conn.commit()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(
    page_title="Messenger",
    layout="wide"
)

st.title("💬 Praveen Messenger")

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Register"]
)

if "user" not in st.session_state:
    st.session_state.user = None

if menu == "Register":

    st.subheader("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):

        try:
            c.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username,password)
            )
            conn.commit()
            st.success("Registered Successfully")

        except:
            st.error("User already exists")

if menu == "Login":

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        user = c.fetchone()

        if user:
            st.session_state.user = username
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Login")

if st.session_state.user:

    st.sidebar.success(
        f"Logged in as {st.session_state.user}"
    )

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.subheader("Chat Room")

    c.execute(
        "SELECT sender,message,filename,timestamp FROM messages ORDER BY id"
    )

    messages = c.fetchall()

    for sender,msg,file,time in messages:

        st.markdown(
            f"**{sender}** ({time})"
        )

        if msg:
            st.write(msg)

        if file:

            filepath = os.path.join(
                UPLOAD_FOLDER,
                file
            )

            ext = file.lower()

            if ext.endswith(
                (".png",".jpg",".jpeg",".gif")
            ):
                st.image(filepath,width=300)

            elif ext.endswith(
                (".mp4",".mov",".avi")
            ):
                st.video(filepath)

            else:
                with open(filepath,"rb") as f:
                    st.download_button(
                        f"Download {file}",
                        f,
                        file_name=file
                    )

        st.divider()

    message = st.text_input("Message")

    uploaded_file = st.file_uploader(
        "Send Image / Video / Document"
    )

    if st.button("Send"):

        filename = ""

        if uploaded_file:

            filename = uploaded_file.name

            with open(
                os.path.join(
                    UPLOAD_FOLDER,
                    filename
                ),
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )

        c.execute(
            """
            INSERT INTO messages(
            sender,
            message,
            filename,
            timestamp
            )
            VALUES(?,?,?,?)
            """,
            (
                st.session_state.user,
                message,
                filename,
                str(datetime.now())
            )
        )

        conn.commit()

        st.rerun()
