import os
import json

from groq import Groq
import pdfplumber



def extract_resume_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"


    return text





def analyze_resume(resume_text):

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )


    prompt = f"""
You are an ATS Resume Analyzer.

Analyze this resume.

Resume:

{resume_text}

Return ONLY valid JSON.
No markdown.
No explanations.
No code blocks.

Use exactly this structure:

{{
    "ats_score": 0,
    "strengths": [],
    "missing_skills": [],
    "recommendations": []
}}
"""


    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2

    )


    response_text = (
        completion
        .choices[0]
        .message
        .content
    )


    print("AI RESUME RESPONSE:")
    print(response_text)



    response_text = response_text.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()



    try:

        return json.loads(
            response_text
        )


    except json.JSONDecodeError:


        return {

            "ats_score": 0,

            "strengths": [],

            "missing_skills": [],

            "recommendations": [
                "AI response was not valid JSON."
            ],

            "raw_response": response_text

        }