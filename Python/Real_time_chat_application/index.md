in SQLite db:
--> conn (connection) - A telephone line to the database
--> cursor (cursor) - your mouth/ear to speak and listen

clients = {
    <WebSocket object 1>: "alice",
    <WebSocket object 2>: "bob"
}

rooms = {
    "#general" : {<websocket 1>, <websocket 2>}, # Both in general
    '#random' : {<websocket 2>} # only bob in random
}

user_ws = {
    "alice" : <WebSocket 1>,
    "bob" : <WebSocket 2>
}

what 'async for msg in broadcast' does:
# this is an infinite loop that:
1. waits for next message from this client
2. when messages arrives, processes it
3. Goes back to waiting
4. Breaks when client disconnects

How Typing indicators work:
--> client-side (browser) sends on every keystroke (<input oninput="typing()">) # user types 'H', 'e', 'l', 'l', 'o'

--> Server broadcasts "typing" to everyone except sender
--> Each client shows "user is typing..." for 2 seconds
--> After 2 seconds, mesage disappears (client-side timeout)

--> Why cleanup matters:
 --> without cleanup:
 --> user disconnects but remains in rooms["#general"]
 --> next broadcast to '#general' tries to send to dead socket
 --> causes errors and memory leaks

--> with cleanup:
 --> All references removed, memory freed, no errors.

 Network interface:
 --> "0.0.0.0" -> listens on all network interface
 --> allows connections from 
   -> localhost(same computer)
   -> LAN IP (192.168.1.x)
   -> Public IP (if configured)


Message Flow Examples:

# User Joins and Sends Message
1. client connects: ws://localhost:8765
2. client sends: {"type": "join", "user":"alice", "room": "#general"}
3. server:
  --> stores connection
  --> fetches history from DB
  --> sends history to alice
4. client sends: {"type": "message", "room": "#general", "text": "Hello!"}
5. server:
  --> saves to DB (room = #general, sender=alice, receiver=None)
  --> Broadcasts to all in room '#general'
6. Other clients receive: {"type": "message", "user"L "alice", "text": "Hello!"}


# Private Message
1. Alice sends: {"type": "dm", "to": "bob", "text": "Sectret message"}
2. Server:
  --> saves to DB (room="DM", sender="alice", receiver: "bob")
  --> checks if bob online (in user_ws)
  --> sends to bob: {"type": "dm", "user": "alice", "text": "secret message"}
  --> sends confirmation to alice
3. Bob receives private message from alice