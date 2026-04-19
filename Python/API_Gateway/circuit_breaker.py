import time
# Track consecutive failures per service
# structure: { "user-service": 3, "order-service": 5}
# like counting how many times each service failed
failures = {} # dictionary type

# Track when each service last failed (for timeout calculation)
# structure {"user-service":14779546245.567, "order-service": 176458457842.123}
last_failed_time = {}

# circuit breaker config
MAX_FAILURES = 5  # Open circuit after 5 consecutive failures
RESET_TIMEOUT = 30 # Try again after 30 seconds

def is_open(service):
    """
    Check if circuit is open for a service.
    
    Circuit States:
     - Closed: Normal operation (requests can go through)
     - Open: Too many failures (requests blocked)
     - Half-Open: After timeout, circuit allows one test request
               -> if success -> back to CLOSED
               -> if failure -> back to OPEN
    
    Returns:
        True: Circuit is OPEN - do not send requests
        False: Circuit is closed or half open - can send requests
    """
    # Get failure count for this service (default 0)
    if failures.get(service, 0) >= MAX_FAILURES:
        
        # check if enough time has passed to try again
        last_failed = last_failed_time.get(service, 0)

        # calculate how much time has passed since last failure
        time_since_failure = time.time() - last_failed

        if time_since_failure > RESET_TIMEOUT:
            # Timeout passed - transition to HALF-OPEN state
            # Return False to allow the next request through for testing
            # if that request succeeds, failures will be reset
            # It it fails, circuit opens again
            print(f"  -> Circuit HALF-OPEN for {service} (timeout passed, testing...)")
            return False  # half-open - let one request through
        else:
            # Still within timeout - circuit remains OPEN
            # Print circuit open message for visibility
            remaining = round(RESET_TIMEOUT - time_since_failure)
            print(f"  -> Circuit OPEN for {service} (blocked, retry in {remaining}s)")
            return True
    # Less than MAX_FAILURES - circuit is CLOSED
    return False


def record_failure(service):
    # Record a failure for a service (increment counter)
    # called when a backend service request fails.
    # increments the failure count and records the failure time.
    
    # increment failure count (default 0 if not exists)
    failures[service] = failures.get(service, 0) + 1

    # record timestamp of this failure
    last_failed_time[service] = time.time()
    
    # Print failure record for visibility
    current = failures[service]
    print(f"  -> Failure #{current}/{MAX_FAILURES} recorded for {service}")
    
    if current >= MAX_FAILURES:
        print(f"  -> CIRCUIT BREAKER TRIPPED! {service} is now OPEN for {RESET_TIMEOUT}s")


def reset(service):
    # Reset failure count after successful request (circuit closes)
    # called when a backend service request succeeds
    # clears the failure counter - circuit returns to CLOSED state.
    
    if failures.get(service, 0) > 0:
        print(f"  -> Success! Circuit CLOSED for {service} (failures reset)")
    # reset the failure count to 0 - service is working again.
    failures[service] = 0