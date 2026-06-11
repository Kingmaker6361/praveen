from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Praveen Messenger</title>

    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

    <style>
        body{
            margin:0;
            font-family:Arial,sans-serif;
            background:#ece5dd;
        }

        .header{
            background:#128C7E;
            color:white;
            text-align:center;
            padding:15px;
        }

        #chat{
            height:70vh;
            overflow-y:auto;
            padding:10px;
        }

        .msg{
            background:white;
            padding:10px;
            margin:8px;
            border-radius:10px;
            box-shadow:0 1px 3px rgba(0,0,0,0.2);
        }

        .bottom{
            position:fixed;
            bottom:0;
            width:100%;
            background:white;
            padding:10px;
            display:flex;
            gap:10px;
        }

        input{
            flex:1;
            padding:10px;
        }

        button{
            background:#128C7E;
            color:white;
            border:none;
            padding:10px 20px;
            cursor:pointer;
        }

        select{
            margin:10px;
            padding:8px;
        }
    </style>
</head>

<body>

<div class="header">
    <h2>Praveen Messenger</h2>
</div>

<select id="user">
    <option>Praveen</option>
    <option>Anuu</option>
</select>

<div id="chat"></div>

<div class="bottom">
    <input id="message" type="text" placeholder="Type message">
    <button onclick="sendMessage()">Send</button>
</div>

<script>

const socket = io();

socket.on("chat_message", function(data){

    let msg = document.createElement("div");
    msg.className = "msg";

    msg.innerHTML =
        "<b>" + data.user + "</b><br>" +
        data.message;

    document.getElementById("chat").appendChild(msg);

    document.getElementById("chat").scrollTop =
        document.getElementById("chat").scrollHeight;
});

function sendMessage(){

    let user =
        document.getElementById("user").value;

    let message =
        document.getElementById("message").value;

    if(message.trim()==="")
        return;

    socket.emit("send_message", {
        user:user,
        message:message
    });

    document.getElementById("message").value="";
}

document.getElementById("message")
.addEventListener("keypress", function(e){
    if(e.key==="Enter"){
        sendMessage();
    }
});

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@socketio.on("send_message")
def handle_message(data):
    emit("chat_message", data, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        allow_unsafe_werkzeug=True
    )
