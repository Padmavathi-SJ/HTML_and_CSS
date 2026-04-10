--> This is a Real-Time IOT Sensor Monitoring System that simulates sensor data (temperature, vibration), processes it in real-time using windows aggregation (moving average, z-score for anomaly detection), and pushes live updates to a web browser dashboard via WebSockets.

Real world use case:
scenario: a factory wants to monitor machine health in real-time
1. sensors attatched to machines measures temperature and vibration
2. system detects when readings exceed normal ranges (anomalies)
3. Operators see live charts and get instant alerts
4. Goal prevent machine breakdown before they happen
   
Sensor Stream -> generates random sendor data every 1 second

Data Processor -> calculates moving avg & z_score to detect anomalies

DWeb dashboard -> isplays live charts and alerts and updates in real time

Moving Avg = sum of last 10 temps / 10\
z-score - (current - avg) / std

-> z-score Interpretation:
|z| < 2: Normal variation
|z| = 2-3: unusual (warning)
|z| > 3: very unusual (critical)

### Workflow:

### Phase 1: Server Startup
1. User runs uvicorn main:app --reload
2. python loads all files
3. FastAPI creates web server on port 8000
4. Lifespan startup runs:
 -> prints "Stream processor started"
 -> prints dashboard URL
 -> creates background task broadcast_sensor_data()
5. Server ready to accept connections

### Phase 2: Browser Connection
1. User opens browser to http://localhost:8000/
2. FastAPI serves dashboard.html to browser
3. Browser loads page and runs Javascript
4. Javascript creates Websocket connection to ws://localhost:8000/ws
5. server accepts connection and adds to connected_clients list
6. console shows "[INFO] 1 client(s) connected"

### Phase 3: Data Generation Loop(every 1 second)

second 1(Reading #1 - NORMAL):
 -> sensor_stream() generates temperature 72.3 degree F
 -> process() calculates: avg =72.3, z=0.0, status="NORMAL"
 -> console prints: [14:05:31] sensor-T1 temp=72.3F vibration=0.12g status=NORMAL
 -> Broadcast to browser via Websocket
 -> browser updates chart with new point at 72.3 degree F(green status)


