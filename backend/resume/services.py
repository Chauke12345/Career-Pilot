import os
import json

import pdfplumber
from groq import Groq



def extract_resume_text(pdf_file):

    text = ""


    try:

        with pdfplumber.open(pdf_file) as pdf:


            for page in pdf.pages:


                page_text = page.extract_text()


                if page_text:

                    text += page_text + "\n"



    except Exception as e:


        print(
            "PDF EXTRACTION ERROR:",
            str(e)
        )


        raise Exception(
            "Could not extract text from PDF"
        )



    if not text.strip():

        raise Exception(
            "No readable text found in PDF"
        )


    return text





def analyze_resume(resume_text):


    api_key = os.environ.get(
        "GROQ_API_KEY"
    )


    if not api_key:


        raise Exception(
            "GROQ_API_KEY is missing"
        )



    client = Groq(
        api_key=api_key
    )



    prompt = f"""
You are an ATS Resume Analyzer.

Analyze this resume.

Resume:

{resume_text}

Return ONLY valid JSON.

No markdown.
No explanations.

Return exactly:

{{
    "ats_score": 0,
    "strengths": [],
    "missing_skills": [],
    "recommendations": []
}}
"""



    try:


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



        print(
            "AI RESUME RESPONSE:"
        )

        print(
            response_text
        )



        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )



        return json.loads(
            response_text
        )



    except Exception as e:


        print(
            "AI ANALYSIS ERROR:",
            str(e)
        )


        return {


            "ats_score": 0,


            "strengths": [],


            "missing_skills": [],


            "recommendations": [

                "Resume analysis failed.",

                str(e)

            ]

        }