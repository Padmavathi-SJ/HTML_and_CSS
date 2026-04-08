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

# start 3 workers
for i in range(1, 4):
    threading.Thread(target=worker_loop, args=(i,), daemon = True).start()
      

time.sleep(1) # Give workers time to start

print("\n=== producer ===")

# enqueue tasks
enqueue("generate_thumbnail", image_id=4521, size=(256, 256))
enqueue("send_email", to="padma@test.com", template="welcome")
enqueue("process_payment", order_id=101, amount=500)

# wait for processing to complete
time.sleep(15)

# show results dashboard
show_dashboard()
