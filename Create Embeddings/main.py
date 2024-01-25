from quixstreams import Application
from sentence_transformers import SentenceTransformer
import os
import time

encoder = SentenceTransformer('all-MiniLM-L6-v2') # Model to create embeddings

# Define the embedding function
def create_embeddings(row):
    text = row['description'] #  Merlin.. i changed this to match the incoming data
    embeddings = encoder.encode(text)
    embedding_list = embeddings.tolist() # Conversion step because SentenceTransformer outputs a numpy Array but Qdrant expects a plain list
    print(f'Created vector: "{embedding_list}"')

    return embedding_list

app = Application.Quix(
    "vectorizer",
    auto_offset_reset="earliest",
    auto_create_topics=True,  # Quix app has an option to auto create topics
)

# Define an input topic with JSON deserializer
input_topic = app.topic(os.environ['input'], value_deserializer="json") #  Merlin! I changed these from "quix" to "json"

# Define an output topic with JSON serializer
output_topic = app.topic(os.environ['output'], value_serializer="json")

# Initialize a streaming dataframe based on the stream of messages from the input topic:
sdf = app.dataframe(topic=input_topic)
sdf = sdf.update(lambda val: print(f"Received update: {val}"))

# Trigger the embedding function for any new messages(rows) detected in the filtered SDF
sdf["embeddings"] = sdf.apply(create_embeddings, stateful=False)

# Update the timestamp column to the current time in nanoseconds
sdf["Timestamp"] = sdf["Timestamp"].apply(lambda row: time.time_ns())

# Publish the processed SDF to a Kafka topic specified by the output_topic object.
sdf = sdf.to_topic(output_topic)

app.run(sdf)