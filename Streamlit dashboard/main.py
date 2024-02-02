import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import os

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

print(os.environ['qdrant_url'])
print(os.environ['qdrant_apikey'])

# Initialize the client with your cloud Qdrant database
client = QdrantClient(
    url=os.environ['qdrant_url'], 
    api_key=os.environ['qdrant_apikey'],
)

collection = os.environ['collectionname']

total_points = client.get_collection(collection_name=collection).points_count
print("---------")
print(total_points)

# Create a text input field for the search term
search_term = st.text_input("Enter your search term")

# Vectorize the search term
query_vector = model.encode([search_term])[0]

# Query the database
search_result = client.search(
    collection_name=collection,
    query_vector=query_vector,
    limit=5
)

print(search_result)
# Display the results in a Streamlit app
st.title('Qdrant Search Results')
st.write(search_result)
#for result in search_result:
#    st.write(f"[ID: {result.id}] {result.payload['phrase']}")
#    st.write(f"Score: {result.score}")
#    st.write("---")

print(f"Total points vectorized {total_points}")