from google import genai
from pydantic import BaseModel
from typing import Optional, List

from config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


class MovieIntent(BaseModel):

    movie: Optional[str] = None

    genres: List[str] = []

    mood: Optional[str] = None

    actors: List[str] = []

    director: Optional[str] = None

    year: Optional[int] = None


def understand_query(query):

    prompt = f"""
You are a movie recommendation intent parser.

Analyze the user's movie request.

Extract:

1. movie
   - Movie explicitly mentioned by the user.
   - If no movie is mentioned, return null.

2. genres
   - Genres requested by the user.

3. mood
   - Emotional, funny, dark, romantic, inspirational,
     scary, relaxing, exciting, etc.
   - If not specified, return null.

4. actors
   - Actors explicitly mentioned by the user.

5. director
   - Director explicitly mentioned by the user.

6. year
   - Specific year requested by the user.
   - If no year is mentioned, return null.

Do not invent information.

User request:

{query}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": MovieIntent
        }
    )

    return MovieIntent.model_validate_json(
        response.text
    )