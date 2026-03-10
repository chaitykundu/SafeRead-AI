import openai
import json

def analyze_book(summary):
    prompt = f"""
Analyze the following book summary for sensitive themes.

Categories:
- Violence
- Profanity
- Sexual Content
- Age Recommendation
- Gender Identity

For each category, provide:
- A rating: Low / Medium / High (or appropriate value for Age Recommendation)
- A short explanation of why you gave that rating

Summary:
{summary}

Return your answer as strict JSON, exactly like this format:

{{
  "violence": {{
    "level": "Low/Medium/High",
    "description": "Explain why"
  }},
  "profanity": {{
    "level": "Low/Medium/High",
    "description": "Explain why"
  }},
  "sexual_content": {{
    "level": "Low/Medium/High",
    "description": "Explain why"
  }},
  "age_recommendation": {{
    "level": "number+",
    "description": "Explain why"
  }},
  "gender_identity": {{
    "level": "Mentioned/Not addressed",
    "description": "Explain why"
  }}
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )

    content = response["choices"][0]["message"]["content"]

    # Attempt to parse the response as JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Sometimes AI includes extra text, try to extract JSON part
        start = content.find("{")
        end = content.rfind("}") + 1
        data = json.loads(content[start:end])

    return data