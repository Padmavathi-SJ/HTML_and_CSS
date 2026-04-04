import time

# sample task 1
def generate_thumbnail(image_id, size):
    time.sleep(1) # simulate work
    return f"/thumbs/{image_id}_{size[0]}*{size[1]}.jpg"

# sample task 2 (fail first 2 times)
retry_counter = {}

def send_email(to, template):
    if to not in retry_counter:
        retry_counter[to] = 0

    retry_counter[to] += 1

    if retry_counter[to] < 3:
        raise Exception("SMTPConnectionError") # simulate failure
    
    return "email_sent"