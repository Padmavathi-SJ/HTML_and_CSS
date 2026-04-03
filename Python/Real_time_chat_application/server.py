import asyncio
import websockets
import json
from collections import defaultdict
from db import create_table, save_message, get_messages

clients = {} #websocket -> username
rooms = defaultdict(set) # room -> websockets
user_ws = {} # username -> websocket

async def broadcast(room, message):
    if room in rooms:
        for client in list(rooms[room]):
            try:
                await client.send(message)
            except:
                rooms[room].remove(client)
            

async def handler(websocket):
    try:
        async for msg in websocket:
            data = json.loads(msg)

            # JOIN ROOM
            if data["type"] == "join":
                username = data["user"]
                room = data["room"]

                clients[websocket] = username
                user_ws[username] = websocket
                rooms[room].add(websocket)

                print(f"{username} joined {room}")

                # send old messages
                history = get_messages(room)
                for sender, message, time in history:
                    await websocket.send(json.dumps({
                        "type": "message",
                        "user": sender,
                        "text": message 
                    }))
            #NORMAL MESSAGE
            elif data["type"] == "message":
                username = clients[websocket]
                room = data["room"]
                text = data["text"]

                save_message(room, username, None, text)

                message = json.dumps({
                    "type": "message",
                    "user": username,
                    "text": text
                })
                
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

                save_message("DM", sender, receiver, text)

                if receiver in user_ws:
                    await user_ws[receiver].send(json.dumps({
                        "type": "dm",
                        "user": sender,
                        "text": text
                    }))

                await websocket.send(json.dumps({
                    "type": "dm",
                    "user": f"(you -> {receiver})",
                    "text": text
                }))
            
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

            for room in rooms:
                rooms[room].discard(websocket)
            
            del clients[websocket]

            if username in user_ws:
                del user_ws[username]



async def main():
    create_table()

    print("Server running on ws://localhost:8765")

    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future() # keeps serevr running forever


if __name__ == "__main__":
    asyncio.run(main())


            