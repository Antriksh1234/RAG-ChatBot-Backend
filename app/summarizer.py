import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_conversation(history: list):

    formatted_history = "\n".join(
        [
            f"{message['role']}: {message['content']}"
            for message in history
        ]
    )

    prompt = f"""
Summarize the following conversation briefly.

Focus only on important topics, decisions, and facts.

Conversation:
{formatted_history}
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

        return response.choices[0].message.content.strip()

    except Exception as e:

        print("SUMMARY ERROR:", str(e))

        return ""