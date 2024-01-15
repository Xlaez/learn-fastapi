from datetime import datetime, timedelta
import random

def random_utc_timestamp():
    current_time = datetime.utcnow()

    random_seconds = random.randint(0, 31536000)  

    direction = random.choice([-1, 1])

    random_timestamp = current_time + direction * timedelta(seconds=random_seconds)

    return random_timestamp

random_timestamp = random_utc_timestamp()
print(random_timestamp)
