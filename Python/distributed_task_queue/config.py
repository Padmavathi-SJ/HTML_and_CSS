import redis # import redis client

# connect to Redis (localhost:6379 default)
redis_client = redis.Redis(
    host="localhost", 
    port=6379, 
    db=0, 
    decode_responses=True,
    password="padmacs253"
    )

QUEUE_NAME = "task_queue" # main queue
DEAD_QUEUE = "dead_letter" # failed tasks
RESULT_KEY = "task_results" # result storage
