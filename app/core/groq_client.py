from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(context, question):
    return client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role":"system","content":"Answer only from context. No guessing."},
            {"role":"user","content":f"Context:\n{context}\n\nQuestion:{question}"}
        ]
    ).choices[0].message.content
