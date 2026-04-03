let ws;
let username;
let room;
let typingTimeout;

function join() {
    username = document.getElementById("username").value;
    room = document.getElementById("room").value;

    document.getElementById("roomName").innerText = room;

    ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
        document.getElementById("status").innerText = "Oneline";

        ws.send(JSON.stringify({
            type: "join",
            user: username,
            room: room
        }));
    };

    ws.onmessage = (event) => {
        let data = JSON.parse(event.data);
        let chat = document.getElementById("chat");

        if(data.type === "message") {
            let div = document.createElement("div");
            div.classList.add("message");

            if(data.user === username) {
                div.classList.add("sent");
            } else {
                div.classList.add("received");
            }

            div.innerHTML = `<b>${data.user}</b><br>${data.text}`;
            chat.appendChild(div);
        }


        if(data.type === "typing") {
            document.getElementById("typing").innerText = 
            `${data.user} is typing...`;

            clearTimeout(typingTimeout);
            typingTimeout = setTimeout(() => {
                document.getElementById("typing").innerText = "";
            }, 2000);
        }

        if(data.type === "dm") {
            let div = document.createElement("div");
            div.classList.add("message", "dm");
            
            div.innerHTML = `<b>[DM] ${data.user}</b><br>${data.text}`;
            chat.appendChild(div);
        }
        chat.scrollTop = chat.scrollHeight;
    };
}

function send() {
    let msg = document.getElementById("msg").value;

    if (!msg) return;

    ws.send(JSON.stringify({
        type: "message",
        "text": msg,
        room: room
    }));

    document.getElementById("msg").value = "";
}

function typing() {
    ws.send(JSON.stringify({
        type: "typing",
        room: room
    }));
}

function sendDM() {
    let to = document.getElementById("to").value;
    let msg = document.getElementById("dm_msg").value;
    
    if(!to || !msg) return;

    ws.send(JSON.stringify({
        type: "dm",
        to: to,
        text: msg
    }));

    document.getElementById("dm_msg").value = "";

}

/* History button */
function loadHistory() {
    ws.send(JSON.stringify({
        type: "history",
        room: room
    }));
}