from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

raw_text = open("data/raw/ticketing.txt", encoding="utf-8").read()

PROMPT = f"""
You are a data extraction assistant.

INPUT TEXT (from Sciqus AMS website):
<<<
{raw_text}
>>>

TASK:
1. Identify the FEATURE NAME.
2. Extract ONLY sub-features explicitly mentioned.
3. Rewrite description in simple language.
4. Do NOT add anything not present in the text.
5. Output VALID JSON only in this format:

{{
  "feature": "...",
  "description": "...",
  "simple_explanation": "...",
  "sub_features": []
}}
"""

response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": PROMPT}]
)

print(response.choices[0].message.content)
