from collections import deque

# store last 10 readings (simulates 5 minutes if each reading is 30 seconds)
# For 1-second intervals, 10 readings = 10 seconds
# Change to 300 for 5 minutes (300 seconds)
window_size = 10
window_data = deque(maxlen=window_size)  # Automatically drops oldest when full

def process(data):
    """
    Process sensor data with sliding window calculations.
    
    Args:
        data: Dictionary with 'temperature', 'vibration', 'sensor'
    
    Returns:
        Dictionary with moving average, z-score, and status
    """
    # Add current reading to window
    window_data.append(data["temperature"])  # Store copy to prevent mutation

    # calculate moving average
    avg_temp = sum(window_data) / len(window_data)

    # calculate moving average
    if len(window_data) > 1:
        variance = sum((x - avg_temp) ** 2 for x in window_data) / len(window_data)
        std_temp = variance ** 0.5   # square root for standard deviation
    else:
        std_temp = 0

    # calculate z-score
    current = data["temperature"]
    if std_temp > 0:
        z_score = (current - avg_temp) / std_temp
    else:
        z_score = 0
    

    # determine status based on temperature
    if current > 100:
        status = "CRITICAL"
    elif current > 85:
        status = "WARNING"
    else:
        status = "NORMAL"
    
    return {
        "avg": round(avg_temp, 2),
        "std": round(std_temp, 2),
        "z": round(z_score, 2),
        "status": status
    }