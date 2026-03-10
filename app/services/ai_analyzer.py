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

    Summary:
    {summary}

    Return short results.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response["choices"][0]["message"]["content"]