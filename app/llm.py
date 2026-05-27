from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_answer(context: str, question: str):

    prompt = f"""
You are a precise AI assistant.

Answer ONLY using the provided context.

Do not make up information.
Do not infer information beyond the exact context.
Do not modify dates, names, or numbers.

If information is not clearly available, say so.

Keep answers concise and factual.

Context:
{context}

Question:
{question}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        answer = response.choices[0].message.content

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        print("GROQ LLM ERROR:", str(e))

        return {
            "success": False,
            "answer": None
        }