import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

response = completion(
    model="groq/llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hello"}],
)

print(response)