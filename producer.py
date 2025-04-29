from fluvio import Fluvio
import json
import datetime
import random

# Connect to Fluvio
fluvio = Fluvio.connect()

# Create a producer for the 'crowd-detection-events' topic
producer = fluvio.topic_producer("crowd-detection-events")

def send_detection(crowd_count):
    timestamp = datetime.datetime.utcnow().isoformat()
    data = {
        "timestamp": timestamp,
        "crowd_count": crowd_count,
        "danger_level": "HIGH" if crowd_count > 80 else "LOW"
    }

    # Convert data to JSON string and send to Fluvio
    json_data = json.dumps(data)
    producer.send_string(json_data)
    print("✅ Message sent:", json_data)

# Example of testing with a crowd_count of 92
send_detection(92)
import time
while True:
    message = {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "crowd_count": random.randint(50, 100),
        "danger_level": "HIGH"
    }
    print(f"Sending message: {message}")
    
    json_data = json.dumps(message)
    producer.send(b'', json_data.encode('utf-8'))


    time.sleep(1)
    from fluvio import Fluvio
import asyncio
import time

async def produce_messages():
    fluvio = await Fluvio.connect()  # Connect to Fluvio
    producer = fluvio.producer("crowd-detection-events")  # Create a producer for the topic

    for i in range(10):  # Produce 10 test messages
        record_value = f"Message {i + 1}"
        await producer.send(record_value.encode())  # Send the message to the topic
        print(f"Sent: {record_value}")
        time.sleep(1)  # Wait for 1 second before sending the next message

    await producer.close()  # Close the producer after sending the messages

# Run the producer
asyncio.run(produce_messages())
