let ws;  // websocket connection object
let username; // current user's name
let room; // current chat room
let typingTimeout; // time for hding typing indicator

function join() {
    username = document.getElementById("username").value;
    room = document.getElementById("room").value;

    document.getElementById("roomName").innerText = room;

    ws = new WebSocket("ws://localhost:8765"); // set global connection

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

        // public msg display
        if(data.type === "message") {
            let div = document.createElement("div");
            div.classList.add("message");

            if(data.user === username) {
                div.classList.add("sent"); // My message  (right aligned)
            } else {
                div.classList.add("received"); // Other's message (left-aligned)
            }

            div.innerHTML = `<b>${data.user}</b><br>${data.text}`;
            chat.appendChild(div);
        }

        //Server broadcasts: {"type": "typing", "user":"Bob"}
        if(data.type === "typing") {
            document.getElementById("typing").innerText = 
            `${data.user} is typing...`; // show "user is typing..."

            clearTimeout(typingTimeout); // clear any existing timer
            typingTimeout = setTimeout(() => {
                document.getElementById("typing").innerText = "";
            }, 2000); // set new timer to hide after 2 seconds
        }
// if user types another key within 2 seconds
// Timer resets
// "user is typing..." stays visible.
// Only disappears 2 seconds after last keystroke

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

    if (!msg) return;  // Don't send empty message

    ws.send(JSON.stringify({ // use same connection from join()
        type: "message",
        "text": msg,
        room: room
    }));

    document.getElementById("msg").value = "";  // Clear input
}

// without lastTypingTime: sends on every keystroke (could be 100+ messages)
// Better: Throttle to send max 1 per second.
let lastTypingTime = 0;

function typing() {
    let now = Date.now();
    if (now - lastTypingTime > 1000) { // 1 second throttle
    ws.send(JSON.stringify({
        type: "typing",
        room: room
    }));
    lastTypingTime = now;
}
}

function sendDM() {
    let to = document.getElementById("to").value;
    let msg = document.getElementById("dm_msg").value;
    
    if(!to || !msg) return; // Both fields required

    ws.send(JSON.stringify({
        type: "dm",
        to: to,
        text: msg
    }));

    document.getElementById("dm_msg").value = ""; // Clear only DM input

}

/* History button */
function loadHistory() {
    ws.send(JSON.stringify({
        type: "history",
        room: room,
        page: page,
        limit: 50
    }));
}