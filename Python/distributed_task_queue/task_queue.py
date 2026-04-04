import json
import uuid
from config import redis_client, QUEUE_NAME

def enqueue(func_name, **kwargs):
    task = {
        "id": str(uuid.uuid4()), # unique task id
        "func": func_name, # function name
        "args": kwargs, # arguments
        "retries": 0, # retry count
        "status": "PENDING" # initial status
    }

    redis_client.rpush(QUEUE_NAME, json.dumps(task)) # push to queue

    # clean enqueue output
    func_display = {
        "generate_thumbnail": "generate_thumbnail",
        "send_email": "send_email"
    }.get(func_name, func_name)

    print(f"Task queued: <Task id={task['id'][:6]} func={func_display} status=PENDING>")