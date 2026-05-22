import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(context: str, question: str):

    prompt = f"""
    Answer the question based only on the provided context.

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