from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Messenger</title>

<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<style>
body{
    margin:0;
    font-family:Arial;
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
    padding:10px;
    margin:5px;
    border-radius:10px;
}

.bottom{
    position:fixed;
    bottom:0;
    width:100%;
    background:white;
    padding:10px;
}

input{
    width:60%;
    padding:10px;
}

button{
    padding:10px;
}
</style>

</head>
<body>

<div class="header">
    <h2>Praveen Messenger</h2>
</div>

<div style="padding:10px;">
<select id="user">
    <option>Praveen</option>
    <option>Anuu</option>
</select>
</div>

<div id="chat"></div>

<div class="bottom">
    <input type="text" id="message" placeholder="Type message">
    <button onclick="sendMessage()">Send</button>
</div>

<script>

const socket = io();

socket.on("chat_message", function(data){

    let div = document.createElement("div");
    div.className = "msg";

    div.innerHTML =
        "<b>" + data.user + "</b>: " +
        data.message;

    document.getElementById("chat").appendChild(div);

    document.getElementById("chat").scrollTop =
        document.getElementById("chat").scrollHeight;
});

function sendMessage(){

    let user =
        document.getElementById("user").value;

    let message =
        document.getElementById("message").value;

    if(message.trim() === "")
        return;

    socket.emit("send_message", {
        user:user,
        message:message
    });

    document.getElementById("message").value="";
}

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
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        allow_unsafe_werkzeug=True
    )
