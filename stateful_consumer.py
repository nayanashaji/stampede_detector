import asyncio
import json
from fluvio import Fluvio
from collections import deque

# Parameters for stateful processing
max_messages = 10  # window size
window = deque(maxlen=max_messages)

# Function to process each message and calculate the average
def process_message(message):
    data = json.loads(message.value())
    crowd_count = data["crowd_count"]
    window.append(crowd_count)
    average = sum(window) / len(window)
    print(f"Processed crowd count: {crowd_count}. Average over last {len(window)} messages: {average:.2f}")

from fluvio import Fluvio, Offset

def main():
    fluvio = Fluvio.connect()
    topic = "crowd-count"  # Replace with your topic name
    consumer = fluvio.partition_consumer(topic, 0)

    # Start consuming from the end (only new messages)
    from fluvio import Offset

    for record in consumer.stream(Offset.beginning()):

        message = record.value_string()
        print(f"Received: {message}")

if __name__ == "__main__":
    main()

