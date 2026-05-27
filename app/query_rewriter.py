import os
from dotenv import load_dotenv

from groq import Groq

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def rewrite_query(
    history: list,
    current_question: str,
    summary: str = ""
):

    if not history:
        return current_question

    formatted_history = "\n".join(
        [
            f"{message['role']}: {message['content']}"
            for message in history
        ]
    )

    prompt = f"""
You are a query rewriting assistant.

Your task is to rewrite the user's latest question into a clear standalone question using the previous conversation context.

Rules:
- ONLY return the rewritten standalone question.
- Do not answer the question.
- Do not explain anything.
- Preserve the original meaning.
- If the latest question is already standalone, return it unchanged.

Conversation Summary:
{summary}

Conversation History:
{formatted_history}

Latest User Question:
{current_question}
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

        rewritten_query = response.choices[0].message.content.strip()

        print("\n--- QUERY REWRITE ---")
        print("Original:", current_question)
        print("Rewritten:", rewritten_query)
        print("--- END QUERY REWRITE ---\n")

        return rewritten_query

    except Exception as e:

        print("QUERY REWRITE ERROR:", str(e))

        return current_question