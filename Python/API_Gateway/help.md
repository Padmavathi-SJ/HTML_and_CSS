This is an API Gateway - a single entry point that sits between clients and multiple background microservices. It handles:
  -> Routing - Directs requests to the correct backend service
  -> Rate Limiting - Prevents abuse by limiting requests per client
  -> Caching - Stores frequeent responses for faster delivery
  -> Circuit Breaker - Stops sending requests to failing services
  -> Health Dashboard - Shows status of all services

Real-world Analogy:
Think of API Gateway as a RECEPTIONIST at a large office buildig:
-> you come to the reception (Gateway)
-> Receptoionist checks your ID badge (Rate Limiting)
-> Looks up which department you and need (Routing)
-> If department is busy/failing, tells you to wait(Circuit Breaker)
-> If someone asked the same question before, gives you the answer from memory (Caching)
-> Keeps a log of which department are working (Dashboard)

What I am building:
Client (browser/App) -> API Gateway -> Backend Services (user services, order services, product services,...)

--> Features:
-> Rate Limiting: 10 requests per minute per API key
-> Caching: GET responses stored for 30-60 seconds
-> Circuit Breaker: Opens after 5 failures, resets after 30 seconds
-> Routing: /api/users/* -> user-service, etc.

### Caching - Response Storage
-> TTL (Time To Live) - How long data stays in cache
-> Cache Hit - Request found in cache
-> Cache Miss - Request not in cache
-> Expiry - When cached data becomes invalid

### Rate Limiting - Token Bucket Algorithm
(10 requests per 60 seconds)
Time 0s = 10 tokens available
time 1s = 9 tokens available (1 consumed)
time 2s = 8 tokens available (2 consumed)
....
time 10s = 0 tokens -> Rate Limited!

After 30 seconds: Refill adds 5 tokens (30/60 * 10 = 5)
after 60 seconds: Refill back to 10 tokens

### Circuit Breaker - Failure Protection
Normal operation (CLOSED):
  Request -> service -> Succes
  failures[service] = 0 (or < 5)
      |
      |
    Failure occurs (5 times)

Circuit Opens (OPEN):
  Request -> Circuit OPEN -> 503 Error
  No calls to failing service
      |
      | 
    After 30 seconds timeout

Test Recovery (HALF-OPEN):
  Request -> service -> If success -> CLOSED
     -> If fail -> OPEN (again)


### Workflow:
### Phase 1: Gateway Startup
1. user runs main file
2. FastAPI creates web server on port 8000
3. Startup function prints gateway information
4. Gateway ready to accept requests

### Phase 2: Request Processing Flow

1. Client sends HTTP request to http://localhost:8000/apiproducts/42
2. Gateway catches requests via wildcard route /{full_path:path}
 
3. Rate limiting chck
  -> extract api key from header (or use "guest)
  -> Call is_allowed(api_key)
  -> token bucket alogorithm checks available tokens
  -> if no tokens -> returns 429 Rate limit exceeded

4. Route Determination
 -> call get_service("/api/products/42")
 -> matches /api/products prefix
 -> Returns service name: "product-service"

5. Circuit Breaker check
 -> call is_open("product-service")
 -> check failure count (starts at 0)
 -> circuit is CLOSED -> continue

6. Cache check (GET requests only)
 -> call get_cache("/api/products/42")
 -> check in-memory cache store
 -> if found and not expired -> CACHE HIT -> Return immediately (2ms)
 -> If not found -> CACHE MISS -> Countinue to backend

7. Backend service call
 -> simulate call to product-service
 -> for order-service, 50% chance of failure (for testing)
 -> if success -> reset failure counter - return response
 -> if failure -> increment failure counter -> return 500 error

8. Cache storage (GET requests only)
 -> after successful responses, call set_cache(path, response, ttl=60)
 -> store in cache_store with expiry timestamp

9. Dashboard update
 -> call show_dashboard() to print current status
 -> shows service health, failures, cache hits

10. Response Returned
 -> JSON response sent back to client

### Phase 3: Circuit breaker Scenario
1. order-service starts failing (50% failure rate)
2. each failure increments failures["order-service"]
3. after 5 failures, failures["order-service"] =5
4. next request calls is_open("order-service")
5. circuit opens -> returns 503 without calling backend
6. after 30 seconds, circuit goes to HALF-OPEN
7. next request allowed through to test service
8. if success -> reset failures to 0 -> circuit CLOSED
9. if failure -> circuit reopens for another 30 seconds

### Phase 4: Rate Limiting Scenario
1. client with API key "client1" sends first request
2. token bucket created with 10 tokens
3. each request concumes with 1 token
4. After 10 requests in 60 seconds, tokens=0
5. next request -> is_allowed() return False
6. Gateway returns 429 Rate Limit Exceeded
7. After 30 seconds, bucket refills 5 tokens (30/60 * 10)
8. More requests allowed untill bucket empty again


### Phase 5: Caching Scenario
1. first GET request to /api/products/42
2. cache miss -> call product-service (134ms)
3. response stored in cache with TTL 60 seconds
4. second GET request to same URL (within 60 seconds)
5. Cache HIT -> return cached response (2ms)
6. Dashboard shows cache hit increment
7. after 60 seconds, cache expires
8. next request triggers cache miss, refreshes cache

--> Reverse Proxy -> clients connect to gateway, not individual services

-> command to run -> uvicorn main:app --reload

curl -X GET "http://localhost:8000/api/products/42" -H "API-KEY: test123"

curl -X GET "http://localhost:8000/api/users/10" -H "API-KEY: user1"

curl -X GET "http://localhost:8000/dashboard" -H "API-KEY: test100"

curl -X GET "http://localhost:8000/api/users/profile" -H "API-KEY: user2"