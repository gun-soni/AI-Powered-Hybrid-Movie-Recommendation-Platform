from google import genai
from config import GEMINI_API_KEY
import json

client = genai.Client(api_key=GEMINI_API_KEY)


def understand_query(query):
    prompt = f"""
You are an AI movie recommendation assistant.

Extract the following information.

Return ONLY valid JSON.

Format:

{{
    "genre":"",
    "mood":"",
    "similar_movie":"",
    "actor":"",
    "director":"",
    "language":"",
    "year":""
}}

User Query:
{query}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )


    text = (response.text.replace("```json", "").replace("```", "").strip())
    
    return json.loads(text)