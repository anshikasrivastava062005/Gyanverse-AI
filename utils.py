import requests

def ask_ai(prompt):
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            
           json={
    "model": "mistral",
    "prompt": prompt,
    "stream": False,
    "options": {
        "num_predict": 100   # limits response length
    }
}
        )

        data = response.json()
        return data.get("response", "No response from AI")

    except Exception as e:
        return f"⚠️ Error: {str(e)}"