# Continuous Vector Ingestion

This template shows you how to continuously ingest documents into a vector store using Apache Kafka. For simplicity, this use case is illustrated by streaming data from small CSV files that represent updates to a book catalog. The descriptive text from the catalog entries is then embedded and then ingested it into a vector store for semantic search. In a production scenario, you might use Change Data Capture (CDC) to ensure that the vector store is in sync with the book catalog database. For more information on the production use cases that is template supports, see the [accompanying blog article](https://quix.io/blog/continuously-ingest-documents-into-a-vector-store-using-quix-qdrant-and-apache-kafka).

This template uses the following open source libraries:

* **Quix** Streams to produce data to, and consume data from, Apache Kafka.

* **Qdrant** to create a database to store embeddings and for basic similarity search

The following screenshot illustrates the architecture of the resulting pipeline in Quix Cloud:
![Pipeline sscreenshot](https://uploads-ssl.webflow.com/64a7eed956ba9b9a3c62401d/65c3777fd9390c70307c3f25_VKG-idlyZnJFKXrhnOdwPTCGtWfE_UE9Lpi2Q4nmidWXBZ40hvpeUeVoxqslaH-5GUR5T69_gYLtn051sHcsptfj2JV5SDlFNkx071kPfBpBo4ZwdRRToNt-pNjQmVeJ57UMP0Yw9ahWLkpL13Cu8Qs.png)

You can also try out a minimal version of this pipeline in a [standalone Jupyter notebook](https://github.com/quixio/tutorial-code/blob/main/notebooks/Continuously_ingest_documents_into_a_vector_store_using_Apache_Kafka.ipynb). 
* To run it Google Colab, click [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/quixio/tutorial-code/blob/main/notebooks/Continuously_ingest_documents_into_a_vector_store_using_Apache_Kafka.ipynb) .


## Trying it out
To try out the pipeline, first clone the vector ingestion template (for more information on how to clone a project template, see the article ["How to create a project from a template in Quix](https://quix.io/blog/how-to-create-a-project-from-a-template"). Before you clone the pipeline, you’ll also need to sign up for a free trial account with [Qdrant Cloud](https://cloud.qdrant.io/) (you can sign up with your GitHub or Google account). When you clone the project template in Quix, you’ll be asked for your Qdrant Cloud credentials.

When running the project, you'll ingest content in two passes, 
* In the **first pass**, you'll add some initial entries to a "book-catalog" vector store via Kafka, then search the vector store (we've used the example query "book like star wars") to check that the data was ingested correctly.
* In the **second round** you'll go through the whole process again (albeit faster) with new data, and see how the matches change for the same search query .

### Run the first ingestion test

1. Press play on the first job (with the name that starts with “PT1…”)—hover your mouse over the “stopped” button to press play.<br><br>
   _This will ingest the first part of the same “sci-fi books” sample dataset that we used in the notebook._ <br><br>
2. On the “Streamlit Dashboard service”, click the blue “launch” icon to open the search UI.<br><br>
3. Search for “book like star wars” — the top result should be “Dune”.<br><br>
   _We can assume it matched because the words in the description are semantically similar to the query: “planet" is semantically close to "star" and "struggles" is semantically close to "wars"._

### Run the second ingestion test

1. Press play on the second job (with the name that starts with “PT2…”)<br><br>
   _This will ingest the second part of the dataset with more relevant matches._ <br><br>
2. In the Streamlit-based search UI, search for “books like star wars” again—the top result should now be “Old man’s war”, and the second result should be “Dune”.<br><br>
   _We can assume that Dune has been knocked off the top spot because the new addition has a more semantically relevant description: the "term" war is almost a direct hit, and "interstellar" is probably semantically closer to the search term "star" than "planet"._
