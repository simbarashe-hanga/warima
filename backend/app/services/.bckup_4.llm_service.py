import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
    model="meta=llama/Llama-3.3-70B-instruct:groq",
    messages=[
        {
            "role": "user",
            "content": ""
        }
    ],
)

print(completion.choices[0].message)
