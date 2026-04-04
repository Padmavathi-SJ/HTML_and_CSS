import pandas as pd  # for calculations

window_data = []  # store last N values (sliding window)

def process(data):
    window_data.append(data)  # add new data

    # keep only last 10 values (moving window)
    if len(window_data) > 10:
        window_data.pop(0)  # remove oldest (FIXED: was pop(10))

    df = pd.DataFrame(window_data)  # convert list → dataframe

    avg_temp = df["temperature"].mean()  # moving average
    std_temp = df["temperature"].std()  # standard deviation

    current = data["temperature"]  # latest value

    # avoid division by zero
    if std_temp == 0:
        z_score = 0
    else:
        z_score = (current - avg_temp) / std_temp  # anomaly score

    # status logic
    if current > 100:
        status = "CRITICAL"
    elif current > 85:
        status = "WARNING"
    else:
        status = "NORMAL"

    return {
        "avg": round(avg_temp, 2),  # moving average
        "z": round(z_score, 2),    # anomaly score
        "status": status           # system status
    }