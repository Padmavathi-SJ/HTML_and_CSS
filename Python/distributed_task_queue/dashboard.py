import json
from config import redis_client, RESULT_KEY, DEAD_QUEUE

def show_dashboard():
    print("\n=== Dashboard ===")
    print("+---------+-------+--------+---------+-----------+")
    print("| Task ID | Func  | Status | Retries | Duration  |")
    print("+---------+-------+--------+---------+-----------+")

    # Get all results from Redis hash
    results = redis_client.hgetall(RESULT_KEY)

    for task_id, data in results.items():
        info = json.loads(data) # Parse JSON string

        # Format for display
        task_short = task_id[:6]  # first 6 chars of UUID
        func = info.get('func', '?')[:5]  # first 5 chars of function name
        status = info['status']
        retries = info['retries']
        duration = f"{info['duration']}s"

        print(f"| {task_short:<8} | {func:<6} | {status:<9} | {retries:<6} | {duration:<11} |")

    # Get all dead letter tasks
    dead_tasks = redis_client.lrange(DEAD_QUEUE, 0, -1) # Get entire list

    for task in dead_tasks:
        t = json.loads(task) # Parse task
        task_short = t['id'][:6]

        # Map function name to display name
        func = {
            "generate_thumbnail": "thumb",
            "send_email": "email"
        }.get(t['func'], t['func'][:5])
        
        print(f"| {task_short:<8} | {func:<6} | {'DEAD_LETTER':<9} | {t['retries']:<6} | {'-':<11} |")
    print("+---------+----------+-------+----------+-------+----------")

