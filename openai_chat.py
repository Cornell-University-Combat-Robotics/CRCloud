import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()
question = "how tall is rohin?"
response = client.chat.completions.create(
    model="gpt-3.5-turbo", 
    messages=[
        # CONTEXT HERE
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{question}"}
    ]
)
print(f"question: {question}")
print(f"answer: {response.choices[0].message.content}")