const socket = io();

const chatBox =
document.getElementById("chat-box");

socket.on(
"receive_message",
function(data){

```
    const div =
        document.createElement("div");

    if(data.sender === USERNAME){

        div.className =
            "message sent";

    }else{

        div.className =
            "message received";
    }

    div.innerHTML = `
        <div class="username">
            ${data.sender}
        </div>

        <div>
            ${data.message}
        </div>
    `;

    chatBox.appendChild(div);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}
```

);

function sendMessage(){

```
const message =
    document.getElementById("message").value;

if(message.trim() === "")
    return;

socket.emit(
    "send_message",
    {
        sender:USERNAME,
        message:message
    }
);

document.getElementById(
    "message"
).value = "";
```

}

document
.getElementById("message")
.addEventListener(
"keypress",
function(e){

```
    if(e.key === "Enter"){
        sendMessage();
    }

}
```

);
