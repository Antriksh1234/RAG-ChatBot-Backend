import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(context: str, question: str):
    prompt = f"""
    You are a precise AI assistant.

    Answer ONLY using the provided context.

    Do not make up information.
    Do not calculate ages unless explicitly stated in the context.
    Do not modify dates or names.
    If information is not clearly available, say so.

    Keep answers concise and factual.

    Context:
    {context}

    Question:
    {question}
    """

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        data = response.json()

        return {
            "success": True,
            "answer": data["response"]
        }

    except Exception as e:

        print("LLM ERROR:", str(e))

        return {
            "success": False,
            "answer": None
        }