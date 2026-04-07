import asyncio  # asyncio handles concurrent connections (many users at once)
import websockets # implementa websocket protocols
import json # convert Python objects <-> json strings for client communication
from collections import defaultdict # dictionary that auto-creates missing keys
from db import create_table, save_message, get_messages

clients = {} #websocket -> username
rooms = defaultdict(set) # room -> set of websockets (set automatically prevents duplicates & allows easy removal)
user_ws = {} # username -> websocket

async def broadcast(room, message): # broadcast function - send to Everyone in Room
    if room in rooms:
        for client in list(rooms[room]): # use list() to avoid modification issues
            try:
                await client.send(message)
            except:
                rooms[room].remove(client)
            

async def handler(websocket):
    try:
        async for msg in websocket: # infine loop
            data = json.loads(msg)

            # JOIN ROOM
            if data["type"] == "join":
                username = data["user"]
                room = data["room"]

                # Register connection in all three data structure

                clients[websocket] = username   # Map socket -> username
                user_ws[username] = websocket # Map username -> socket
                rooms[room].add(websocket)   # Add socket to room

                print(f"{username} joined {room}")

                # send old messages (send msg history to this user only)
                history = get_messages(room)
                for sender, message, time in history:
                    await websocket.send(json.dumps({
                        "type": "message",
                        "user": sender,
                        "text": message 
                    }))

            #NORMAL MESSAGE
            elif data["type"] == "message":
                username = clients[websocket]   # who sent this?
                room = data["room"]  # which room?
                text = data["text"]  # Message content

                # save to database (receier=None for public messages)
                save_message(room, username, None, text)

                # create JSON for broadcasting
                message = json.dumps({
                    "type": "message",
                    "user": username,
                    "text": text
                })

                # send to everyone in the room
                await broadcast(room, message)

            # TYPING INDICATOR
            elif data["type"] == "typing":
                username = clients[websocket]
                room = data["room"]

                message = json.dumps({
                    "type": "typing",
                    "user": username
                })

                await broadcast(room, message)
            
            #PRIVATE MESSAGE
            elif data["type"] == "dm":
                sender = clients[websocket]
                receiver = data["to"]
                text = data["text"]

                # save with receier specified (not null)
                save_message("DM", sender, receiver, text)

                # send to receiver if online
                if receiver in user_ws:
                    await user_ws[receiver].send(json.dumps({
                        "type": "dm",
                        "user": sender,
                        "text": text
                    }))

                # confirm to sender
                await websocket.send(json.dumps({
                    "type": "dm",
                    "user": f"(you -> {receiver})",
                    "text": text
                }))
            
            # History Retrieval(like if new user has joined in a room)
            elif data["type"] == "history":
                room = data["room"]
                history = get_messages(room)

                for sender, message, time in history:
                    await websocket.send(json.dumps({
                        "type": "message",
                        "user": sender,
                        "text": message
                    }))


    except Exception as e:
        print("Error:", e)
        

    finally:
        if websocket in clients:
            username = clients[websocket]
            print(f"{username} disconnected")

            # Remove from all rooms
            for room in rooms:
                rooms[room].discard(websocket)
            
            # Remove from lookup dictionaries
            del clients[websocket]

            if username in user_ws:
                del user_ws[username]



async def main():
    create_table()  # ensure database exists

    print("Server running on ws://localhost:8765")

    # Start websocket server
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future() # keeps server running forever (A future that never completes = run forever (waits indefinitely))


if __name__ == "__main__":
    asyncio.run(main())


            