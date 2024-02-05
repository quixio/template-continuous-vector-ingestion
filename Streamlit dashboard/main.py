import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import os
import time

# import the dotenv module to load environment variables from a file
#from dotenv import load_dotenv
#load_dotenv(override=False)

try:
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
    #st.write(search_result[0])
    for result in search_result:
        st.write(f"[ID: {result.id}] {result.payload['name']} - {result.payload['author']}")
#        if "description" in result:
#            st.write(f"{result.description}")
        st.write(f"Score: {result.score}")
        st.write("---")

    print(f"Total points vectorized {total_points}")

    while True:
        time.sleep(1)
except Exception as e:
        print(f"Exception: {e}")