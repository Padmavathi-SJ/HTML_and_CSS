import redis # import redis client
import os
from dotenv import load_dotenv

load_dotenv()

# connect to Redis (localhost:6379 default)
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),  # Redis server address (same machine)
    port=int(os.getenv("REDIS_PORT", 6379)),  # Default Redis port
    db=int(os.getenv("REDIS_DB", 0)),  # Database number (0-15 available)
    decode_responses=True, # Automatically decode bytes to strings
    password=os.getenv("REDIS_PASSWORD", None) # Authentication password
    )

QUEUE_NAME = os.getenv("QUEUE_NAME", "task_queue") # main queue for pending tasks
DEAD_QUEUE =  os.getenv("DEAD_QUEUE", "dead_letter") # Queue for permanenetly failed tasks
RESULT_KEY =  os.getenv("RESULT_HASH", "task_results") # Hash key for storing task results

def clear_old_results():
    redis_client.delete(QUEUE_NAME)
    redis_client.delete(DEAD_QUEUE)
    redis_client.delete(RESULT_KEY)
    print("cleared old data from Redis")