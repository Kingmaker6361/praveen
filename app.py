import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template_string
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
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
    height:75vh;
    overflow-y:auto;
    padding:10px;
}

.msg{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:10px;
}

.bottom{
    position:fixed;
    bottom:0;
    width:100%;
    background:white;
    display:flex;
    gap:10px;
    padding:10px;
}

input{
    flex:1;
    padding:10px;
}

button{
    padding:10px 20px;
    background:#128C7E;
    color:white;
    border:none;
    cursor:pointer;
}

select{
    margin:10px;
    padding:5px;
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
<input type="text" id="message" placeholder="Type message">
<button onclick="sendMessage()">Send</button>
</div>

<script>

const socket = io();

socket.on("connect", function() {
    console.log("Connected");
});

socket.on("message", function(data){

    const div = document.createElement("div");
    div.className = "msg";

    div.innerHTML =
        "<b>" + data.user + "</b><br>" +
        data.text;

    document.getElementById("chat").appendChild(div);

    document.getElementById("chat").scrollTop =
        document.getElementById("chat").scrollHeight;
});

function sendMessage(){

    const user =
        document.getElementById("user").value;

    const text =
        document.getElementById("message").value;

    if(text.trim() === "")
        return;

    socket.send({
        user:user,
        text:text
    });

    document.getElementById("message").value="";
}

document
.getElementById("message")
.addEventListener("keypress", function(e){
    if(e.key === "Enter"){
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

@socketio.on("message")
def handle_message(data):
    send(data, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(
        app,
        host="0.0.0.0",
        port=port
    )
