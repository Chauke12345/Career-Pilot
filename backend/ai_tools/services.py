import os
import json
from groq import Groq


def analyze_job_description(job_description):

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    prompt = f"""
You are an AI career assistant.

Analyze this job description:

{job_description}

Return ONLY valid JSON with this structure:

{{
    "skills_found": [],
    "match_score": 0,
    "missing_skills": [],
    "recommendation": ""
}}

Identify:
- technical skills mentioned
- missing skills a developer should learn
- estimated match percentage
- career advice
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        return {
            "skills_found": [],
            "match_score": 0,
            "missing_skills": [],
            "recommendation": result
        }