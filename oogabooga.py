import chromadb
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from openai import OpenAI
import json


# func 1: processing data, return collection

# func 2: query -> vectorizing -> connecting query with data and llm
# inputs: user_text: str, vectorized_data, 
class Ooga:

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()
        self.embedding_function = SentenceTransformer("multi-qa-mpnet-base-dot-v1") # modify this for different encoding type
        #self.chroma_client = chromadb.Client()
        self.chroma_client = chromadb.Client(
            settings=chromadb.config.Settings(anonymized_telemetry=False)
        )
        self.collection = self.create_data()

    def create_data(self):
        hashmap = {}
        with open("json_data/janfab_data.json", 'r') as file:
                hashmap = json.load(file)

        docs = list(hashmap.values())
        ids = list(hashmap.keys())

        embeddings = []
        for doc in docs:
            embeddings.append(self.embedding_function.encode(doc).tolist())

        # switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
        collection = self.chroma_client.get_or_create_collection(name="my_collection")
        collection.upsert(
            embeddings=embeddings,
            documents=docs,
            ids=ids
            )
        return collection
    
    def query(self, user_text, num_results = 3):
        query_embedding = self.embedding_function.encode(user_text).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=num_results # how many results to return
        )
        context = ""
        for i in range(0, num_results):
            context += f"{results['documents'][0][i]} \n"
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                # CONTEXT HERE
                {"role": "system", "content": "You are a helpful RAG assistant for cornell's combat robotics team (CRC). Answer questions about our documentation, and explain your reasoning behind each answer. if you are not confident in your answer, say you dont know. You may also answer non crc related questions. Here is your context: " + context},
                {"role": "user", "content": f"{user_text}"}
            ]
        )

        return response.choices[0].message.content
        
