from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager  # NEW: Import for lifespan
import asyncio
from datetime import datetime

from sensor import sensor_stream
from processor import process

# store connected clients
connected_clients = []

# LIFESPAN CONTEXT MANAGER (replaces @app.on_event)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages startup and shutdown events.
    Code before yield runs at startup.
    Code after yield runs at shutdown.
    """
    # --- STARTUP (runs once when server starts) ---
    print("[INFO] Stream processor started — consuming from sensors/factory-a")
    print("[INFO] Dashboard available at http://localhost:8000/")
    
    # Start the background streaming task
    task = asyncio.create_task(broadcast_sensor_data())
    
    # Yield control to the application
    yield
    
    # --- SHUTDOWN (runs when server stops) ---
    print("[INFO] Shutting down...")
    task.cancel()  # Stop the streaming task
    await task  # Wait for it to finish
    print("[INFO] Stream processor stopped")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


# Serve Dashboard HTML

@app.get("/")
async def get_dashboard():
    """Serve the dashboard HTML page"""
    with open("templates/dashboard.html", "r") as f:
        return HTMLResponse(f.read())


# WebSocket Connection

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time updates"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    print(f"[INFO] {len(connected_clients)} client(s) connected")
    
    try:
        # Keep connection alive
        while True:
            await asyncio.sleep(1)
    except:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"[INFO] Client disconnected ({len(connected_clients)} remaining)")


async def broadcast_sensor_data():
    # Main loop: get data, process it, send to clients
    
    print("\n=== Live sensor Feed (every 1s) ===")

    async for sensor_data in sensor_stream():

        # process the data
        processed = process(sensor_data)

        # Get timestamp
        now = datetime.now().strftime("%H:%M:%S")

        # print to console
        print(f"[{now} sensor--{sensor_data['sensor']}  "
              f"temp={sensor_data['temperature']}F  "
              f"vibration={sensor_data['vibration']}g  "
              f"status={processed['status']}")
        
        # Trigger alert for critical
        if processed["status"] == "CRITICAL":
            print(f"\n=== Alert Triggered ===")
            print(f"[ALERT] sensor-{sensor_data['sensor']} - Temperature exceeded threshold (>100F)")
            print(f"Current: {sensor_data['temperature']}F | "
                  f"5-min avg: {processed['avg']}F | "
                  f"Deviation: +{processed['z']} sigma")
            print(f"Action:  Notification sent to ops-team@factory.com\n")


        # Merge for output
        output = {
            "sensor": sensor_data["sensor"],
            "temperature": sensor_data["temperature"],
            "vibration": sensor_data["vibration"],
            "avg": processed["avg"],
            "z": processed["z"],
            "status": processed["status"]
        }


        # send to all connected clients
        for client in connected_clients[:]: # copy list to avoid modification issues
            try:
                await client.send_json(output)
            except:
                if client in connected_clients:
                    connected_clients.remove(client)
        
        # wait 1 second before next reading
        await asyncio.sleep(1)
                           

   