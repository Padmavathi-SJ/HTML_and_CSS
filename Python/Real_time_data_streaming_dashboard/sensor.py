import random  # generate random values
import asyncio  # for async delay

# async generator → produces data continuously
async def sensor_stream():
    while True:  # infinite loop (real-time stream)
        data = {
            "sensor": "T1",  # sensor id
            "temperature": round(random.uniform(60, 110), 2),  # random temperature
            "vibration": round(random.uniform(0.1, 0.6), 2)  # random vibration
        }

        yield data  # send data to caller (main.py)

        await asyncio.sleep(1)  # wait 1 second