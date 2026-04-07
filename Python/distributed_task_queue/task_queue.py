import json # for serializing tasks to JSON
import uuid # for generating unique task IDs
from config import redis_client, QUEUE_NAME

def enqueue(func_name, **kwargs):
    """
    Adds a task to the Redis queue.
    
    Args:
        func_name: Name of the functionto execute (string)
        **kwargs: Arguments to pass to the function
        
    Example:
        enqueue("generate_thumnail", image_id=4521, size(256,256))
    """
    # Create Task Dictionary
    task = {
        "id": str(uuid.uuid4()), # unique task id
        "func": func_name, # function name
        "args": kwargs, # arguments
        "retries": 0, # initial retry count
        "status": "PENDING" # initial status
    }
    # rpush = right push (adds to end of list)
    # Queue is FIFO (first in,first out)
    redis_client.rpush(QUEUE_NAME, json.dumps(task)) # push to queue

    # clean enqueue output 
    func_display = {
        "generate_thumbnail": "generate_thumbnail",
        "send_email": "send_email"
    }.get(func_name, func_name)

    print(f"Task queued: <Task id={task['id'][:6]} func={func_display} status=PENDING>")