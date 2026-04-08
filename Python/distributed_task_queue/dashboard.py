import json
from config import redis_client, RESULT_KEY

def show_dashboard():
    print("\n=== DASHBOARD ===")
    print("+---------+--------+-------------+---------+-----------+")
    print("| Task ID | Func   | Status      | Retries | Duration  |")
    print("+---------+--------+-------------+---------+-----------+")

    results = redis_client.hgetall(RESULT_KEY)

    for task_id, data in results.items():
        info = json.loads(data)

        print(f"| {task_id[:6]:<8} | "
              f"{info['func']:<6} | "
              f"{info['status']:<11} | "
              f"{info['retries']:<7} | "
              f"{str(info['duration'])+'s':<9} |")

    print("+---------+--------+-------------+---------+-----------+")