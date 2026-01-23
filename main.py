# {"title": str, "content": str}
# 1. load data
# 2. vectorize
# 3. chat chat chat

import chromadb
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

embedding_function = SentenceTransformer("multi-qa-mpnet-base-dot-v1") # modify this for different encoding type
chroma_client = chromadb.Client()

hashmap = {}
with open("json_data/janfab_data.json", 'r') as file:
        hashmap = json.load(file)

docs = list(hashmap.values())
ids = list(hashmap.keys())

embeddings = []
for doc in docs:
    embeddings.append(embedding_function.encode(doc))

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(name="my_collection")

# switch `add` to `upsert` to avoid adding the same documents every time
# collection.upsert(
#     documents=[
#         "Riddhi is on the Autonomous team",
#         "Rohin is on the Autonomous team",
#         "Rohin doesn't believe in free will",
#         "Anika does believe in free will",
#         "Anika is on the Autonomous team"
#     ],
#     ids=["id1", "id2","id3", "id4", "id5"]
# )

collection.upsert(
    embeddings=embeddings,
    documents=docs,
    ids=ids
)

while(True):
    query = input("Ask away! Enter exit to quit\n ")

    if (query == "exit"):
        break
    
    num_results = 3

    query_embedding = embedding_function.encode(query)

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=num_results # how many results to return
    )


    context = ""

    for i in range(0, num_results):
        context += results["documents"][0][i]

    print(context)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            # CONTEXT HERE
            {"role": "system", "content": "You are a helpful RAG assistant. Here is your context: " + context},
            {"role": "user", "content": f"{query}"}
        ]
    )
    print(f"question: {query}")
    print(f"answer: {response.choices[0].message.content}")
