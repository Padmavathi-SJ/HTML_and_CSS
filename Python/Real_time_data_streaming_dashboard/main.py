from fastapi import FastAPI, WebSocket  # FIXED: WebSocket (capital S)
from fastapi.responses import HTMLResponse
import asyncio
from datetime import datetime 

from sensor import sensor_stream  # sensor generator
from processor import process     # processing logic

app = FastAPI()  # create FastAPI app

clients = []  # store connected clients

# =========================
# Serve Dashboard HTML
# =========================
@app.get("/")
async def get():
    with open("templates/dashboard.html") as f:
        return HTMLResponse(f.read())  # FIXED: f.read() was f.need()

# =========================
# WebSocket Connection
# =========================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # accept connection
    clients.append(websocket)  # store client

    print(f"[INFO] {len(clients)} client(s) connected")

    try:
        while True:
            await asyncio.sleep(1)  # keep connection alive
    except:
        clients.remove(websocket)  # remove if disconnected
        print(f"[INFO] client disconnected ({len(clients)} remaining)")

# =========================
# Background Streaming Task
# =========================
@app.on_event("startup")
async def start_stream():

    async def stream():
        print("=== Live sensor feed (every 1s) ===")

        async for data in sensor_stream():  # get sensor data

            result = process(data)  # process data

            output = {**data, **result}  # merge dicts

            # =========================
            # FORMAT CONSOLE OUTPUT
            # =========================
            time_str = datetime.now().strftime("%H:%M:%S")

            print(
                f"[{time_str}] sensor-{data['sensor']}  "
                f"temp={data['temperature']}F  "
                f"vibration={data['vibration']}g  "
                f"status={result['status']}"
            )

            # ======================
            # ALERT LOGIC
            # ======================
            if result["status"] == "CRITICAL":
                print("\n=== Alert Triggered ===")
                print(
                    f"[ALERT] sensor-{data['sensor']} - Temperature exceeded threshold (>100F)"
                )
                print(
                    f"Current: {data['temperature']}F | "
                    f"Avg: {result['avg']}F | "
                    f"Deviation: +{result['z']} sigma"
                )
               

            # send data to all connected clients
            for client in clients:
                await client.send_json(output)

    asyncio.create_task(stream())  # run in background