import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Distance, VectorParams
import numpy as np
from qdrant_client.models import PointStruct


# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the client with your cloud Qdrant database
# client = QdrantClient(":memory:")
client = QdrantClient(
    url="https://1242ba45-04ba-4852-9afe-5c39e284d3f0.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="s8N2shKMgRxyvTF3RGcUDDPbAKDP9MOF8zBNYng0BpynCBMsUCozow",
)

total_points = client.get_collection(collection_name="demo_collection").points_count
print("---------")
print(total_points)

# Create a text input field for the search term
search_term = st.text_input("Enter your search term")

# Vectorize the search term
query_vector = model.encode([search_term])[0]

# Query the database
search_result = client.search(
    collection_name="demo_collection",
    query_vector=query_vector,
    limit=5
)

print(search_result)
# Display the results in a Streamlit app
st.title('Qdrant Search Results')
for result in search_result:
    st.write(f"[ID: {result.id}] {result.payload['phrase']}")
    st.write(f"Score: {result.score}")
    st.write("---")

print(f"Total points vectorized {total_points}")