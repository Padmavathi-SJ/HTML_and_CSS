from fastapi import FastAPI, Request # FastAPI framework and request object
from fastapi.responses import JSONResponse  # Return JSON responses
import time  # for requestion duration tracking
import random # to simulating random failures for demo

# importing all Gateway components
from rate_limiter import is_allowed
from cache import get_cache, set_cache
from circuit_breaker import is_open, record_failure, reset, MAX_FAILURES  # ADDED MAX_FAILURES here
from router import get_service
from dashboard import show_dashboard, increment_cache

# create FastAPI application instance
# FastAPI - modern, fast web framework for building APIs
app = FastAPI()

# IMPORTANT: Dashboard route MUST be defined BEFORE the catch-all route
# FastAPI matches routes in order of definition
@app.get("/dashboard")
def dashboard():
    # manual dashboard trigger endpoint
    show_dashboard()
    return {"message": "Dashboard printed in console"}

@app.on_event("startup")
def startup():
    print("\n=== Gateway Startup ===")
    print("Api Gateway running on http://127.0.0.1:8000")
    print("Routes loaded: ")
    print("/api/users/**    -> user-service")
    print("/api/orders/**   -> order-service")
    print("/api/products/** -> product-service")
    print("/dashboard       -> Health Dashboard")
    print("\nRate Limit: 10 requests per 60 seconds per API key")
    print("Circuit Breaker: Opens after 5 failures, resets after 30 seconds\n")
    

# Catch ALL routes - this is a "catch-all" route that handles every request
# @app.api_route = handles ANY HTTP method (GET, POST, PUT, DELETE, etc.)
# This MUST be the LAST route defined
@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request: Request, full_path: str):
    """
    Main Gateway handler - processes all incoming requests

    Steps:
    1. Extract request info
    2. Rate limiting check
    3. Route determination
    4. Circuit breaker check
    5. Cache check (for GET requests)
    6. Forward to backend services 
    7. Store in cache (for GET responses)
    8. Return response      
    """
    # step 1: extract request information
    start = time.time()   # Track request start time for latency calculation
    path = "/" + full_path  # Reconstruct full path

    # Get API key from request header (or use 'guest' as default)
    # API key identifies which client is making request
    api_key = request.headers.get("API-KEY", "guest")  
    
    
    # step 2: RATE LIMITING CHECK
    if not is_allowed(api_key):
        # Rate limit exceeded - client has made too many requests
        # Return HTTP 429 too many requests
        duration = round((time.time() - start) * 1000, 2)
        print(f"[REQ] {request.method} {path} client={api_key} -> RATE LIMITED - 429 Too Many Requests in {duration}ms")
        return JSONResponse(
            {"error": "Rate limit exceeded", "retry_after": 60}, 
            status_code=429
        )


    # step 3 - ROUTING
    # find which backend service should handle this request
    service = get_service(path)
    if not service:
        # No matching route - return 404 not found
        duration = round((time.time() - start) * 1000, 2)
        print(f"[REQ] {request.method} {path} -> NO ROUTE - 404 Not Found in {duration}ms")
        return JSONResponse(
            {"error": "Service not found"}, 
            status_code=404
        )


    # step 4: CIRCUIT BREAKER CHECK
    if is_open(service):
        # circuit is open - service is failing, don't forward request
        # Return HTTP 503 Service Unavailable with retry suggestion
        duration = round((time.time() - start) * 1000, 2)
        print(f"[REQ] {request.method} {path} client={api_key} -> CIRCUIT OPEN ({service}) - 503 Service Unavailable in {duration}ms")
        return JSONResponse(
            {"error": "Service temporarily unavailable", "retry_after": 30},
            status_code=503
        )


    # step 5 - CACHE CHECK (GET requests only)
    # POST, PUT, DELETE requests modify data, so they shouldn't be cached
    if request.method == "GET":
        cached, ttl = get_cache(path)

        if cached is not None:   
            # CACHE HIT - return cached response
            increment_cache(service)  # Track for dashboard
            duration = round((time.time() - start) * 1000, 2)
            print(f"[REQ] {request.method} {path} client={api_key} -> CACHE HIT (TTL: {ttl}s remaining) - 200 OK in {duration}ms")
            show_dashboard()  # Update dashboard after each request
            return JSONResponse(cached)


    # step 6: forward to BACKEND service
    try:
        # For demo purposes, we simulate backend responses with random failures
        # this tests circuit breaker without needing actual microservices
        
        # Configure failure rates per service for testing
        # order-service: 80% failure rate to easily trigger circuit breaker
        # user-service: 20% failure rate
        # product-service: 10% failure rate
        
        if service == "order-service":
            # 80% failure rate for order-service (aggressive for testing circuit breaker)
          
                # Simulate failure without raising exception directly
                # Use the exception handler pattern
            raise Exception("Order service database connection failed")
        
        elif service == "user-service":
            # 20% failure rate for user-service
            if random.random() < 0.2:
                raise Exception("User service timeout")
        
        elif service == "product-service":
            # 10% failure rate for product-service
            if random.random() < 0.1:
                raise Exception("Product service unavailable")
        
        # simulate successful backend response
        response = {
            "service": service,
            "data": f"Response from {service}",
            "path": path,
            "timestamp": time.time()
        }

        # Success - reset failure counter for this service
        reset(service)

        # calculate request duration 
        duration = round((time.time() - start) * 1000, 2) # milliseconds

        # log successful request
        print(f"[REQ] {request.method} {path} client={api_key} -> PROXY to {service} - 200 OK in {duration}ms")

    except Exception as e:
        # Failure - record for circuit breaker
        record_failure(service)

        # calculate duration even for failures
        duration = round((time.time() - start) * 1000, 2)
        error_msg = str(e)
        print(f"[REQ] {request.method} {path} client={api_key} -> FAILED to {service} ({error_msg}) - 500 Error in {duration}ms")
        
        # Get current failure count for display
        from circuit_breaker import failures
        current_failures = failures.get(service, 0)
        print(f"  -> Circuit breaker: {current_failures}/{MAX_FAILURES} failures for {service}")
        
        if current_failures >= MAX_FAILURES:
            print(f"  -> WARNING: CIRCUIT OPEN for {service}! Next requests will be blocked for 30 seconds")

        return JSONResponse({"error": "Service failure"}, status_code=500)

    # step 7: STORE IN CACHE (GET requests only)
    if request.method == "GET":
        # Cache successful GET responses for 60 seconds
        # future identical requests will hit cache instead of calling backend
        set_cache(path, response, ttl=60)
    
    # step 8: Update dashboard and return responses
    show_dashboard()
    return JSONResponse(response)