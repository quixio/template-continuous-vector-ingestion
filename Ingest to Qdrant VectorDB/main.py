from quixstreams.kafka import Producer
from quixstreams import Application, State, message_key
from sentence_transformers import SentenceTransformer
from qdrant_client import models, QdrantClient

qdrant = QdrantClient(path="./scifi-books4") # persist a Qdrant DB on the filesystem

# Create collection to store books
qdrant.recreate_collection(
    collection_name="my_books",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(), # Vector size is defined by used model
        distance=models.Distance.COSINE
    )
)

# Define the ingestion function
def ingest_vectors(row):

  single_record = models.PointStruct(
    id=row['doc_uuid'],
    vector=row['embeddings'],
    payload=row
    )

  qdrant.upload_points(
      collection_name="my_books",
      points=[single_record]
    )

  print(f'Ingested vector entry id: "{row["doc_uuid"]}"...')

app = Application(
    broker_address="127.0.0.1:9092",
    consumer_group="vectorizer3",
    auto_offset_reset="earliest",
    consumer_extra_config={"allow.auto.create.topics": "true"},
)

# Define an input topic with JSON deserializer
input_topic = app.topic(inputtopicname, value_deserializer="json")

# Initialize a streaming dataframe based on the stream of messages from the input topic:
sdf = app.dataframe(topic=input_topic)

# INGESTION HAPPENS HERE
### Trigger the embedding function for any new messages(rows) detected in the filtered SDF
sdf = sdf.update(lambda row: ingest_vectors(row))
app.run(sdf)