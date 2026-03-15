import openai
import json

def analyze_book(summary):

    prompt = f"""
You are a Child Content Safety Expert.

Your task is to evaluate the following book summary
specifically for CHILDREN.

Categories:
- Violence
- Profanity
- Sexual Content
- Age Recommendation
- Gender Identity

For each category provide:
- level
- short explanation

When writing the "message", match the tone to the content level and be specific:
- Mention the exact types of content found (e.g. fantasy violence, dark themes, romantic scenes)
- Reference the book's context when possible
- Keep it to 1-2 sentences max
- Be specific enough for a parent to make an informed decision

Examples:
- Safe: "This book is appropriate for children. It contains no violence, profanity, or mature themes."
- Caution: "This book contains mild fantasy violence and references to dark magic. Themes of death and loss are present but handled age-appropriately."  
- Concerning: "This book contains multiple instances of graphic violence including death and combat scenes. Strong themes of survival and trauma throughout. Parental guidance is strongly recommended."

Summary:
{summary}

Return JSON only in this format:

{{
  "violence": {{"level":"None/Mild/High","description":"Explain"}},
  "profanity": {{"level":"None/Mild/High","description":"Explain"}},
  "sexual_content": {{"level":"None/Mild/High","description":"Explain"}},
  "age_recommendation": {{"level":"number+","description":"Explain"}},
  "gender_identity": {{"level":"Mentioned/Not addressed","description":"Explain"}},
  "message": "1-2 sentence specific and descriptive child-safety summary."
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
        "None": 90,
        "Mild": 60,
        "High": 20
    }

    # ✅ Weighted scoring — most critical for child safety
    weights = {
        "sexual_content": 0.45,   # 45% — most critical
        "violence":       0.40,   # 40% — serious
        "profanity":      0.15    # 15% — least critical
    }

    weighted_score = 0
    for cat, weight in weights.items():
        level = data.get(cat, {}).get("level", "None")
        score = score_map.get(level, 90)
        weighted_score += score * weight

    overall_score = int(weighted_score)

    # ✅ High override — any High forces Red
    if any(
        data.get(cat, {}).get("level") == "High"
        for cat in ["violence", "profanity", "sexual_content"]
    ):
        rating = "Red"
        text = "Concern"
        overall_score = min(overall_score, 39)

    # ✅ Mild override — any Mild forces at least Yellow
    elif any(
        data.get(cat, {}).get("level") == "Mild"
        for cat in ["violence", "profanity", "sexual_content"]
    ):
        rating = "Yellow"
        text = "Caution"
        overall_score = min(overall_score, 60)

    # ✅ All None → use weighted score naturally
    else:
        if overall_score < 40:
            rating = "Red"
            text = "Concern"
        elif overall_score <= 60:
            rating = "Yellow"
            text = "Caution"
        else:
            rating = "Green"
            text = "Safe"

    message = data.pop("message", "No summary available.")

    data["overall_score"] = {
        "percentage": overall_score,
        "rating": rating,
        "text": text,
        "message": message
    }

    return data