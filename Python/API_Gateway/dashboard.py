from circuit_breaker import failures, last_failed_time
import time

# Track cache hits per service for dashboard
# Structure: {"user-service": 1204, "order-service": 302}
cache_hits = {
    "user-service": 0,
    "order-service": 0,
    "product-service": 0
}


def increment_cache(service):
    # increment cache hit counter for a service
    # called every time we successully used cached response
    # Used to calculate the cache effetiveness in dashboard (ex: counting how many times I grabed leftovers from fridge instead of cooking fresh.)
    cache_hits[service] += 1


def show_dashboard():
    """
    Display health dashboard showing service status, failures, and cache hits.
    
    This provides real-time visibility into:
    - which services are UP or DOWN
    - Circuit breaker states (OPEN/CLOSED)
    - cache effectiveness per service
    """
    print("\n=== Health Dashboard ===")
    print("+------------------+--------+----------+-----------+-------------+")
    print("| Service          | Status | Failures | Circuit   | Cache Hits  |")
    print("+------------------+--------+----------+-----------+-------------+")

    # Iterate through all backend services
    for service in ["user-service", "order-service", "product-service"]:
        # get failure count for each service
        fail = failures.get(service, 0)
        
        # determine service status based on failure count
        if fail >= 5:
            status = "DOWN"  # service has failed too many times
            circuit = "OPEN"  # circuit breaker is blocking requests
            # Calculate time until circuit resets
            last_failed = last_failed_time.get(service, 0)
            time_since = time.time() - last_failed
            reset_in = max(0, 30 - round(time_since))
            reset_text = f"reset in {reset_in}s"
        else:
            status = "UP"  # service is working
            circuit = "CLOSED" # Circuit breaker is closed(allows requests)
            reset_text = ""

        # Print service row with status
        status_display = status
        if status == "DOWN":
            status_display = "DOWN"
        
        print(f"| {service:<16} | {status_display:<6} | {fail:<8} | {circuit:<9} | {cache_hits[service]:<11} | {reset_text}")

    print("+------------------+--------+----------+-----------+-------------+")
    print(f"Total Cache Hits: {sum(cache_hits.values())}")
    print("")