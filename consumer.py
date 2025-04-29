import json
from fluvio import Fluvio

# Initialize Fluvio connection
fluvio = Fluvio.connect()

# Create a topic consumer for 'crowd-detection-events'
try:
    # Here we will use the consumer method with the `topic_consumer` instead
    consumer = fluvio.topic_consumer("crowd-detection-events")

    # Continuously consume messages
    while True:
        record = consumer.poll()

        if record:
            # Decode the message into a dictionary
            message = json.loads(record.value)

            # Extract and print the crowd count and danger level
            crowd_count = message['crowd_count']
            print(f"Received crowd count: {crowd_count}")

            # Further processing can be done here (e.g., determining danger level)

except Exception as e:
    print(f"Error: {e}")
