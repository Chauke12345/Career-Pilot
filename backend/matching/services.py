import os
import json

from groq import Groq



def analyze_match(resume_text, job_description):


    client = Groq(
        api_key=os.environ.get(
            "GROQ_API_KEY"
        )
    )


    prompt = f"""

You are an AI career matching assistant.

Compare this resume:

RESUME:

{resume_text}


Against this job description:

JOB DESCRIPTION:

{job_description}


Return ONLY valid JSON.

Format:

{{
"match_score":0,
"matching_skills":[],
"missing_skills":[],
"recommendation":""
}}

"""


    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.2

    )


    response = (
        completion
        .choices[0]
        .message
        .content
    )


    response = response.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()


    return json.loads(response)