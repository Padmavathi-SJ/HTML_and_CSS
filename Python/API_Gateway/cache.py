import time  # for TTL(Time To Live) calculation

# In-memory cache storage
# Structure: {"cache-key": (response_data, expiry_timestamp)}
cache_store = {}  # in-memory cache

def get_cache(key):
    """
    Retrive cached response if not expired
    Args:
        Key: URL path(eg: "/api/products/42")
    Returns:
        tuple: (cached_data, remaining_seconds) or (None, 0) if miss/expired
    """
    # check if key exists in cache
    if key in cache_store:
        # unpack the stored tuple
        value, expiry = cache_store[key]
        # calculating how many seconds remaining untill expiry
        remaining = expiry - time.time()

        # if still valid
        if remaining > 0:
            return value, round(remaining)  # return data and remaining TTL
        else:
            # Expired - remove from cache to save memory
            del cache_store[key]
    # Cache miss or expired
    return None, 0  # cache miss

def set_cache(key, value, ttl=30):
    """
    Store responses in cache with expiration time.
    Args:
        key: URL path to use as cache key
        value: Response data to store
        ttl: time to live in seconds (default 30)
    """
    # calculate expiration timestamp = current time + TTL
    expiry = time.time() + ttl # set expiry time

    # store tuple of (value, expire_time)
    cache_store[key] = (value, expiry)
