import os, json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_with_llm(text: str):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extrae SOLO estos campos en JSON:\n"
                    "name, pizza, size, quantity, drink, delivery_type, address, confirmation\n"
                    "Si no aparece, usa null."
                )
            },
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    return json.loads(completion.choices[0].message.content)