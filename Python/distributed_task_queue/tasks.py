import time # for simulating work duration

# sample task 1
def generate_thumbnail(image_id, size):
    time.sleep(1) # simulate work
    return f"/thumbs/{image_id}_{size[0]}*{size[1]}.jpg"

# sample task 2 (fail first 2 times)
retry_counter = {} # Global dictionary to track retries per email

def send_email(to, template):
    # Initialize counter for this receipient if not exists
    if to not in retry_counter:
        retry_counter[to] = 0

    # increment attempt counter
    retry_counter[to] += 1

    # Fail first 2 attempts
    if retry_counter[to] < 3:
        raise Exception("SMTPConnectionError") # simulate connection failure
    
    # successs on 3rd attempt
    return "email_sent"