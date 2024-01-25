# This code will publish the CSV data to a stream as if the data were being generated in real-time.

# Import the supplimentary Quix Streams modules for interacting with Kafka: 
from quixstreams.kafka import Producer
from quixstreams.platforms.quix import QuixKafkaConfigsBuilder, TopicCreationConfigs
from quixstreams.models.serializers.quix import JSONSerializer, QuixSerializer, SerializationContext

# (see https://quix.io/docs/quix-streams/v2-0-latest/api-reference/quixstreams.html for more details)

from datetime import datetime
import pandas as pd
import threading
import random
import time
import os
import uuid
import json

# Load the CSV file
df = pd.read_csv('documents.csv')

with Producer(
    broker_address="127.0.0.1:9092",
    extra_config={"allow.auto.create.topics": "true"},
) as producer:
    for index, row in df.iterrows():
                
        if shutting_down: # If shutdown has been requested, exit the loop.
            break
        row_data = {header: row[header] for header in headers} # Create a dictionary that includes both column headers and row values
        row_data['Timestamp'] = int(time.time() * 1e9) # add a new timestamp column with the current data and time 
        # (MC: Why though? wanna know "why" rather than "what"- i.e. we need the time in nanoseconds)

        # publish the row via the wrapper function
        publish_row(stream_id, row_data)

        print(f"Producing value: {value}")
        producer.produce(
            topic=outputtopicname,
            headers=[("uuid", doc_uuid)],  # a dict is also allowed here
            key=doc_key,
            value=json.dumps(value),  # needs to be a string
        )
        time.sleep(0.2)

# Run the CSV processing in a thread
processing_thread = threading.Thread(target=process_csv_file, args=("demo-data.csv",))
processing_thread.start()

# Run this method before shutting down.
# In this case we set a flag to tell the loops to exit gracefully.
def before_shutdown():
    global shutting_down
    print("Shutting down")

    # set the flag to True to stop the loops as soon as possible.
    shutting_down = True


print("Exiting.")