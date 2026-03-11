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

For each category provide:
- level
- short explanation

Summary:
{summary}

Return JSON only in this format:

{{
  "violence": {{"level":"Low/Medium/High","description":"Explain"}},
  "profanity": {{"level":"Low/Medium/High","description":"Explain"}},
  "sexual_content": {{"level":"Low/Medium/High","description":"Explain"}},
  "age_recommendation": {{"level":"number+","description":"Explain"}},
  "gender_identity": {{"level":"Mentioned/Not addressed","description":"Explain"}}
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response["choices"][0]["message"]["content"]

    # Parse JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}") + 1
        data = json.loads(content[start:end])

    # Convert ratings to scores
    score_map = {
        "Low": 90,
        "Medium": 60,
        "High": 20
    }

    scores = []

    for cat in ["violence", "profanity", "sexual_content"]:
        level = data.get(cat, {}).get("level", "Low")
        scores.append(score_map.get(level, 90))

    # Calculate overall percentage
    overall_score = int(sum(scores) / len(scores))

    # Assign rating
    if overall_score < 40:
        rating = "Red"
    elif overall_score <= 60:
        rating = "Yellow"
    else:
        rating = "Green"

    # Generate dynamic message
    issues = [cat for cat, score in score_map.items() if score > 50]  # categories above threshold

    if issues:
        issues_text = ", ".join(issues)
        message = f"This book contains noticeable content in the following areas: {issues_text}. Please review carefully."
    else:
        message = "This book appears safe with minimal sensitive content."

    # Add overall result
    data["overall_score"] = {
        "percentage": overall_score,
        "rating": rating,
        "message": message
    }

    return data