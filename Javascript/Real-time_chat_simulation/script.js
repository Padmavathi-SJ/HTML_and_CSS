const chatWindow = document.getElementById("chatwindow");

//Get current time
function getTime() {
    const now=new Date();
    return now.toLocaleTimeString([], {hour:'2-digit', minute: '2-digit'});
}

//Display message
function addMessage(text, type) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", type);

    msgDiv.innerHTML = `
    ${text}
    <div class="time"> ${getTime()}</div>
    `;

    chatWindow.appendChild(msgDiv);

    //Auto scroll
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

//Send Message
function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();

    if(text === "") return;

    addMessage(text, "sent");
    input.value = "";

    //Simulate reply
    simulateReply();
}

//Simulate incoming messages
function simulateReply() {
    const replies = [
        "Hello!",
        "How are you?",
        "That's interesting.",
        "Can you tell me more?",
        "I see.",
        "Thanks for sharing!",
        "Let's catch up soon.",
        "Okay Okay",
        "Sounds good!",
        "Talk to you later!",
        "Have a great day!"
    ];

    const randomReply = replies[Math.floor(Math.random() * replies.length)];

    setTimeout(() => {
        addMessage(randomReply, 'received');
    }, 1000 + Math.random() * 2000);
}

//Optional: Auto incoming messages every few seconds
setInterval(() => {
    const autoMessages = ["Hey!", "What's up?", "Ping!", "Are you there?"];
    const msg = autoMessages[Math.floor(Math.random() * autoMessages.length)];
    addMessage(msg, "received");
}, 10000);