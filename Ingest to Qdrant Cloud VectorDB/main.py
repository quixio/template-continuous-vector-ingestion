from quixstreams import Application
from sentence_transformers import SentenceTransformer
from qdrant_client import models, QdrantClient
import os

qdrant = QdrantClient(
    url="https://620342be-1e5e-401c-98da-42bcaddaed57.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key=os.environ['qdrant_apikey'],
)

encoder = SentenceTransformer('all-MiniLM-L6-v2') # Model to create embeddings
collection = os.environ['collectionname']

# Create collection to store items
qdrant.recreate_collection(
    collection_name=collection,
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
      collection_name=collection,
      points=[single_record]
    )

  print(f'Ingested vector entry id: "{row["doc_uuid"]}"...')

app = Application.Quix(
    "vectorizer",
    auto_offset_reset="earliest",
    auto_create_topics=True,  # Quix app has an option to auto create topics
)

# Define an input topic with JSON deserializer
input_topic = app.topic(os.environ['input'], value_deserializer="json") # Merlin.. i updated this for you

# Initialize a streaming dataframe based on the stream of messages from the input topic:
sdf = app.dataframe(topic=input_topic)

# INGESTION HAPPENS HERE
### Trigger the embedding function for any new messages(rows) detected in the filtered SDF
sdf = sdf.update(lambda row: ingest_vectors(row))
app.run(sdf)