import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_book(summary):

    prompt = f"""
    Analyze the following book summary for sensitive themes.

    Categories:
    - Violence
    - Profanity
    - Sexual Content
    - Age Recommendation
    - Gender Identity
    - category

      For each category, provide:
    - A rating: Low / Medium / High (or appropriate value for Age Recommendation)
    - A short explanation of why you gave that rating

    Summary:
    {summary}

    Return short results in JSON format like:
    {{
        "violence": "Low/Medium/High",
        "profanity": "Low/Medium/High",
        "sexual_content": "Low/Medium/High",
        "age_recommendation": "X+",
        "gender_identity": "Mentioned/Not addressed"
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response["choices"][0]["message"]["content"]