import json
import time
import uuid
from config import redis_client, QUEUE_NAME, DEAD_QUEUE, RESULT_KEY
import tasks # import task functions

MAX_RETRIES = 3

def exponential_backoff(retries):
    return 2 ** retries # 2, 4, 8 seconds

def process_task(task):
    func_name = task["func"] # get function name
    args = task["args"] # get arguments
    func = getattr(tasks, func_name) # dynamically get function

    # Map function names to display names
    func_display = {
        "generate_thumbnail": "thumb",
        "send_email": "email"
    }.get(func_name, func_name[:5])

    start = time.time()

    try:
        result = func(**args) # execute function

        duration = round(time.time() - start, 2)

        print(f"[WORKER-{task.get('worker_id', '?')}] Task {task['id'][:6]} completed in {duration}s - result: {result}")
    

        redis_client.hset(RESULT_KEY, task["id"], json.dumps({
            "status": "SUCCESS",
            "result": result,
            "retries": task["retries"],
            "duration": duration,
            "func": func_display

        }))

    except Exception as e:
        task["retries"] += 1
        error_msg = str(e).replace("Exception: ", "")

        if task["retries"] > MAX_RETRIES:
            print(f"[WORKER-{task.get('worker_id', '?')}] Task {task['id'][:6]} DEAD_LETTER - retries exhausted")

            redis_client.rpush(DEAD_QUEUE, json.dumps(task))

        else:
            delay = exponential_backoff(task["retries"])

            print(f"[WORKER-{task.get('worker_id', '?')}] Task {task['id'][:6]} FAILED ({error_msg}) -retry {task['retries']}/{MAX_RETRIES} in {delay}s")

            time.sleep(delay)

            redis_client.rpush(QUEUE_NAME, json.dumps(task))


def worker_loop(worker_id):
    print(f"=== Worker {worker_id} ===")

    while True:
        task_json = redis_client.lpop(QUEUE_NAME) # get task

        if task_json:
            task = json.loads(task_json)
            task['worker_id'] = worker_id
            func_display = {
                "generate_thumbnail": "generate_thumbnail",
                "send_email": "send_email"
            }.get(task["func"], task["func"])

            print(f"[WORKER-{worker_id}] Picked up task {task['id'][:6]} ({func_display})")

            process_task(task)

        
        else:
            time.sleep(1) # wait if queue empty
