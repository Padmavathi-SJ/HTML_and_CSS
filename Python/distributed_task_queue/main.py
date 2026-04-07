import threading # for running workers in parallel
from task_queue import enqueue
from worker import worker_loop
from dashboard import show_dashboard
import time
from config import redis_client, clear_old_results

# clear old data before starting
clear_old_results()

# show broker info
print("=== Broker ===")
print("[BROKER] Listening on redis://localhost:6379/0")
print(f'[WORKER] Queue "default" - {redis_client.llen("task_queue")} pending, 2 workers connected')
print("5. Python")
print("6")

print("\n=== Producer ===")

      
# start 2 workers as daemon threads
threading.Thread(target=worker_loop, args=(1,), daemon=True).start()
threading.Thread(target=worker_loop, args=(2,),  daemon=True).start()

time.sleep(1) # Give workers time to start

# enqueue tasks
enqueue("generate_thumbnail", image_id=4521, size=(256, 256))
enqueue("send_email", to="padma@test.com", template="welcome")

# wait for processing to complete
time.sleep(10)

# show results dashboard
show_dashboard()
