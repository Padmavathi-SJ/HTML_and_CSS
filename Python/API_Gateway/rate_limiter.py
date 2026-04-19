import time

# Dictionary to store token buckets for each API key
# Each API key gets its own bucket (fair per-client limiting)
# Structure: {"api_key_123": {"token": 10, "last": timestamp}}
buckets = {}

# Rate limiting configuration
RATE = 10       # Number of requests allowed in the given time window
WINDOW = 60     # Time window in seconds (10 requests per 60 seconds)


def is_allowed(api_key):
    """
    Token bucket rate limiter
    Returns Ture if request is allowed, False if rate limited
    
    How Token Bucket works:
    1. Bucket holds up to RATE tokens
    2. Tokens refill at rate of RATE/WINDOW per second
    3. Each request consumes 1 token
    4. If no tokens available -> rate limited
    """
    now = time.time()  # current timestamp

    # First request from this API key - create new bucket if not exists
    if api_key not in buckets:
        buckets[api_key] = {
            "tokens": RATE,  # start with full bucket
            "last": now      # Lat refill time
        }

    bucket = buckets[api_key]

    # Calculate how many tokens to add based on time elapsed
    elapsed = now - bucket["last"] # seconds since last refill
    
    # Refill rate = (elapsed seconds / window seconds) * rate
    # ex: 10 seconds elapsed, 60 seconds window, 10 rate
    # ( 10 / 60 )* 10 = 1.67 tokens to add
    refill = (elapsed / WINDOW) * RATE

    # Add tokens but never exceed maximum RATE
    bucket["tokens"] = min(RATE, bucket["tokens"] + refill)
    
    # Update last refill time
    bucket["last"] = now

    # check if we have atleast 1 token available
    if bucket["tokens"] < 1:
        return False  # Rate limited - no tokens left

    # consume 1 token for this request
    bucket["tokens"] -= 1
    return True  # Request allowed