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
    "confirmed_skills": [],
    "related_skills": [],
    "missing_skills": [],
    "confidence_score": 0,
    "recommendation": ""
}}

Analyze:

- confirmed_skills:
  Skills the candidate already has.

- related_skills:
  Transferable skills that relate to the role.

- missing_skills:
  Skills required by the job but missing.

- confidence_score:
  Realistic compatibility percentage.

- recommendation:
  Career improvement advice.
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
            "confirmed_skills": [],
            "related_skills": [],
            "missing_skills": [],
            "confidence_score": 0,
            "recommendation": result
        }