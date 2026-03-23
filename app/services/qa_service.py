from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"

def generate_answer(context, question):
    prompt = f"""
You are an AI assistant analyzing a video transcript.

IMPORTANT RULES:
- For general questions, infer the main topic from overall context
- For specific questions, answer precisely from context
- If partial info exists, still answer intelligently
- DO NOT say "Not found" unless absolutely no info is present

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content