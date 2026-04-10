import random
import asyncio # allows asynchronous operations (non-blocking delays)

# async generator function -> produces data continously
async def sensor_stream():
    """
    Async generator that produces simulated sensor data.
    Can be extended to support multiple sensors.
    """
   # Track how many readings we've sent
    reading_count=0

    while True:
        reading_count += 1
       
         
        # create pattern to trigger alerts
        # every 15-29 readings, create a spike
        if reading_count % 15 == 0:
            # SPIKE - This will trigger CRITICAL
            temperature = random.uniform(102, 110) # Above 100 degree F
            
        elif reading_count % 8 == 0:
            # WARN - This will trigger WARNING
            temperature = random.uniform(86, 99)  # above 85 degree F
           
        else:
            # NORMAL - Normal operation
            temperature = random.uniform(65, 84)  # Normal range
          
        
        data = {
            "sensor": "T1",
            "temperature": round(temperature, 2),
            "vibration": round(random.uniform(0.1, 0.6), 2)
          
        }

        yield data
        await asyncio.sleep(1)  # Send every second
