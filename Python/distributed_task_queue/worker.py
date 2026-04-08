import json # for parsing tasks
import time # for delays and timing
from config import redis_client, QUEUE_NAME, DEAD_QUEUE, RESULT_KEY
import tasks # import task functions to execute
import random 

MAX_RETRIES = 3 # Maximum number of retry attempts

def exponential_backoff(retries):
    return 2 ** retries # 2, 4, 8 seconds

def process_task(task):
    """
    Executes a single task with retry logic.
    Args:
        task: Dictionary containing task information
    """
    # Extract task information
    func_name = task["func"] # get function name string
    args = task["args"] # get arguments dictionary
    func = getattr(tasks, func_name) # dynamically get function object

    # Map function names to display names
    func_display = {
        "generate_thumbnail": "thumb",
        "send_email": "email",
        "process_payment": "pay"
    }.get(func_name, func_name[:5])

    start = task.get("start_time", time.time())  # keep original start

    try:
        # Execute the function with unpacked arguments
        result = func(**args) # (**args) unpacks dictionary to keyword arguments

        duration = round(time.time() - start, 2) # calculate duration

        print(f"[WORKER-{task.get('worker_id', '?')}] Task {task['id'][:6]} completed in {duration}s - result: {result}")
    
        # store success result in Redis hash
        redis_client.hset(
            RESULT_KEY, 
            task["id"], 
            json.dumps({
            "status": "SUCCESS",
            "result": result,
            "retries": task["retries"],
            "duration": duration,
            "func": func_display
        })
)

    except Exception as e:
        task["retries"] += 1 # Increment retry counter
        error_msg = str(e).replace("Exception: ", "")

        if task["retries"] > MAX_RETRIES:
            duration = round(time.time() - start, 2)

            print(f"[WORKER-{task.get('worker_id', '?')}] Task {task['id'][:6]} DEAD_LETTER - retries exhausted")

            # Move to dead letter queue (permanent failure)
            redis_client.hset(
                RESULT_KEY, 
                task["id"], 
                json.dumps({
                "status": "DEAD_LETTER",
                "result": None,
                "retries": task["retries"],
                "duration": duration,
                "func": func_display
            })
)


        else:
            delay = exponential_backoff(task["retries"]) # calculate wait time

            elapsed = round(time.time() - start, 2)

            print(f"[WORKER-{task.get('worker_id', '?')}] Task {task['id'][:6]} FAILED ({error_msg}) -retry {task['retries']}/{MAX_RETRIES} in {delay}s (elapsed {elapsed}s)")

            time.sleep(delay) # wait before retrying

            # Re-queue the task for another attempt
            redis_client.rpush(QUEUE_NAME, json.dumps(task))


# Worker Loop - Continue Task Processing
def worker_loop(worker_id):
    """
    Main worker loop that continously polls for tasks.
    Args:
        worker_id
    """
    print(f"=== Worker {worker_id} ===")

    while True: # Infinite loop - runs forever
        # Try to get a task from the queue (non-blocking)
        task_json = redis_client.lpop(QUEUE_NAME) # get task

        if task_json:
            # Parse task from JSON
            task = json.loads(task_json)
            task['worker_id'] = worker_id # Tag with worker ID
            
            # Display task pickup message
            func_display = {
                "generate_thumbnail": "generate_thumbnail",
                "send_email": "send_email",
                "process_payment": "process_payment"
            }.get(task["func"], task["func"])

            print(f"[WORKER-{worker_id}] Picked up task {task['id'][:6]} ({func_display})")

            # process the task
            process_task(task)

        
        else:
            time.sleep(random.uniform(0.5, 1.5)) # wait if queue empty, before polling again. and this distributes load better across workers
