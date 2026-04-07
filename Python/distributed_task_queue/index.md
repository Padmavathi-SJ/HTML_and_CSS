Distributed Task Queue System - A system for distributing and executing tasks across multiple worker processes.
 --> Queue tasks (functions) to be executed asynchromously
 --> Distribute them across multiple worker processes
 --> Handle failures with retries
 --> Store results for later retrieval

Example:
Restaurant Kitchen = Tour Task Queue System
Customer orders (Producers) -> OderSlips (Queue) -> Chefs (Workers) -> Completed dishes (Results)
If chef burns dish (Failure) -> Try again (Retry) -> If keeps failing -> Dead Letter (Trash)

### Redis
--> In-memory data structure store used as:
1. Message broker (queue)
2. Database (for results)
3. cache
   

Redis Data Structure Used:
--> QUEUE_NAME - List (FIFO queue)
 redis_client.lpush/QUEUE_NAME # add to queue
 redis_client.rpop/QUEUE_NAME # emove from queue

--> DEAD_QUEUE - List (stores failed tasks)
 redis_client.lpush/DEAD_QUEUE

--> RESULT_KEY - Hash (key-value pairs)
 redis_client.hset(RESULT_KEY, task_id, result) # Store result
 redis_client.hgetall(RESULT_KEY) # Get all results


### Failure Simulation Flow:
--> First call:
send_email("bob@test.com", "welcome")  # Raises Exception

--> Second call (retry):
send_email("bob@test.com", "welcome")  # Raises Exception

--> Third call (retry):
send_email("bob@test.com", "welcome")  # Returns "email_sent"

### Redis List Operations:
--> Producer: rpush (add to right)
redis_client.rpush("task_queue", task1) # [task1]
redis_client.rpush("task_queue", task2) # [task1, task2]

--> Worker: lpop (remove from left)
redis_client.lpop("task_queue) # Returns task1, queue becomes [task2]

### Worker - Consumer Logic
--> Without backoff (fixed 1 second):
 --> Task fails → retry after 1s → fails → retry after 1s → fails...
 --> Can overwhelm the system

--> With exponential backoff:
 --> Task fails → 2s wait → fails → 4s wait → fails → 8s wait
 --> Gives system time to recover

getattr():
--> tasks module has functions: generate_thmbnail, send_email
--> func_name = "generate_thmbnail"
func = getattr(tasks, "generate_thumbnail")
--> Now func() is the same as tasks.generate_thumbnail()

--> Equivalent to:
if func_name == "generate_thumbnail":
    func = tasks.generate_thmbnail
elif func_name == "send_email":
    func = tasks.send_email


**args Unpacking:
--> args = {"image_id": 4521, "size": (256, 256)}
--> Equivalent to: generate_thumbnail(image_id=4521, size=(256, 256))

lpop va blpop:
--> lpop (non-blocking) - returns None if queue empty
task = redis_client.lpop("task_queue)
if task is None:
  time.sleep(1) # Manual wait

--> blpop (blocking) - waits until task arrived
task = redis_client.blpop("task_queue", timeout=0) # waits forever

lrange:
--> lrange(key, start, end) - Get range of list elements
redis_client.lrange("dead_letter", 0, -1)  # 0 = first, -1 = last (all elements)
redis_client.lrange("dead_letter", 0, 9)   # First 10 elements
redis_client.lrange("dead_letter", -5, -1) # Last 5 elements

### Daemon Threads:
--> Regular thread: Prevents program from exiting
thread = threading.Thread(target=worker_loop, args=(1,))
thread.start()
--> Program waits for this thread to finish (never happens - infinite loop)

--> Daemon thread: Dies when main program ends
thread = threading.Thread(target=worker_loop, args(1, ), daemon=true)
thread.start()
--> Program can exit even if thread is running

### producer-Consumer Pattern
--> producer (main.py): Creates tasks
enqueue("task", data=value) # Produces work

--> Consumer (worker.py): Processes tasks
task = redis_client.lpop(QUEUE_NAME) # consumer work
process_task(task)


### FIFO Queue(first-in-first-out)
# Order of operations:
redis_client.rpush("queue", "first")   # Queue: ["first"]
redis_client.rpush("queue", "second")  # Queue: ["first", "second"]
redis_client.rpush("queue", "third")   # Queue: ["first", "second", "third"]

redis_client.lpop("queue")  # Returns "first"  (first in)
redis_client.lpop("queue")  # Returns "second" (second in)
redis_client.lpop("queue")  # Returns "third"  (third in)

### Exponential Backoff
--> Why not fixed delay?
Fixed delay (2s):
Attempt 1: fail at 0s → retry at 2s
Attempt 2: fail at 2s → retry at 4s  
Attempt 3: fail at 4s → retry at 6s
--> Too aggressive, may overwhelm system

Exponential backoff:
Attempt 1: fail at 0s → retry at 2s   (2^1)
Attempt 2: fail at 2s → retry at 6s   (2^2 = 4s later)
Attempt 3: fail at 6s → retry at 14s  (2^3 = 8s later)
--> Gives system time to recover

### Dead Letter Queue (DLQ)
--> purpose: store tasks that permanently failed
--> prevents: Infinite retry loops
--> Allows: Manual inspection and debugging

if retries > MAX_RETRIES:
  redis_client.rpush(DEAD_QUEUE, task) # Move to DLQ
--> Task won't be processed again

### Task Serialization
Why JSON?
-> Python objects cannot be sent to Redis directly

--> Encode (serialize):
task_dict = {"func": "generate_thumbnail", "args": {...}}
task_json = json.dumps(task_dict) # '{"func": "generate_thumbnail", ...}'
redis_client.rpush(QUEUE_NAME, task_json)

-- > Decode (deserialize):
task_json = redis_client.lpop(QUEUE_NAME)
task_dict = json.loads(task_json) # Back to Python dict

### Threading for Concurrency
--> without threading (sequential):
worker1() --> Runs forever, blocks everything else
worker2() --> Never reaches this line

--> With threading (parallel):
threading.Thread(target=worker1).start()  --> Runs in background
threading.Thread(target=worker2).start() --> Also runs in background
--> Both workers run simultaneously

--> commands to run
using bash terminal --> 
wsl
redis-server requirepass 'password'
then in vs terminal - python main.py