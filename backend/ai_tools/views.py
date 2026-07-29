import os
import json


import pdfplumber
from docx import Document

from groq import Groq


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import (
    api_view,
    permission_classes
)


from drf_spectacular.utils import extend_schema


from .serializers import (
    JobAnalyzerSerializer,
    AssistantSerializer
)


from .services import analyze_job_description



# ======================================
# GROQ CLIENT
# ======================================

def get_groq_client():

    api_key = os.environ.get(
        "GROQ_API_KEY"
    )

    if not api_key:

        raise Exception(
            "GROQ_API_KEY missing from environment variables"
        )


    return Groq(
        api_key=api_key
    )




# ======================================
# CLEAN AI JSON RESPONSE
# ======================================

def clean_json_response(text):

    try:

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        return json.loads(
            text.strip()
        )


    except Exception:

        return {

            "error":
            "AI returned invalid JSON",

            "raw":
            text

        }





# ======================================
# RESUME TEXT EXTRACTION
# ======================================

def extract_resume_text(file):

    text = ""


    try:

        filename = file.name.lower()



        if filename.endswith(".pdf"):


            with pdfplumber.open(file) as pdf:


                for page in pdf.pages:


                    page_text = page.extract_text()


                    if page_text:

                        text += (
                            page_text
                            +
                            "\n"
                        )



        elif filename.endswith(".docx"):


            document = Document(file)


            for paragraph in document.paragraphs:

                text += (
                    paragraph.text
                    +
                    "\n"
                )



        elif filename.endswith(".txt"):


            text = file.read().decode(
                "utf-8",
                errors="ignore"
            )


    except Exception as e:


        print(
            "Resume extraction error:",
            e
        )



    return text.strip()






# ======================================
# JOB DESCRIPTION ANALYZER
# ======================================

class JobAnalyzerView(APIView):


    permission_classes = [
        IsAuthenticated
    ]



    def post(self, request):


        serializer = JobAnalyzerSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )



        job_description = serializer.validated_data[
            "job_description"
        ]



        result = analyze_job_description(
            job_description
        )



        return Response(
            result
        )






# ======================================
# RESUME QUALITY ANALYZER
# ======================================

class ResumeAnalyzerView(APIView):


    permission_classes = [
        IsAuthenticated
    ]



    def post(self, request):


        resume = request.FILES.get(
            "resume"
        )



        if not resume:

            return Response(
                {
                    "error":
                    "No resume uploaded"
                },
                status=400
            )



        resume_text = extract_resume_text(
            resume
        )



        if not resume_text:


            return Response(
                {
                    "error":
                    "Could not extract CV text"
                },
                status=400
            )



        client = get_groq_client()



        prompt = f"""

You are an expert ATS resume reviewer.

Review this CV for a Junior Full-Stack Developer position.

CV:

{resume_text}


Return ONLY JSON:

{{
"resume_quality_score":0,
"strengths":[],
"weaknesses":[],
"recommendations":[]
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



        data = clean_json_response(

            completion.choices[0].message.content

        )



        return Response(
            data
        )








# ======================================
# CV JOB MATCH
# ======================================

class MatchResumeView(APIView):


    permission_classes = [
        IsAuthenticated
    ]



    def post(self, request):


        resume = request.FILES.get(
            "resume"
        )


        job_description = request.data.get(
            "job_description"
        )



        if not resume or not job_description:


            return Response(

                {
                    "error":
                    "Resume and job description required"
                },

                status=400

            )




        resume_text = extract_resume_text(
            resume
        )



        if not resume_text:


            return Response(

                {
                    "error":
                    "Could not extract resume text"
                },

                status=400

            )





        client = get_groq_client()



        prompt = f"""


You are an ATS recruitment system.

Compare this resume with this job description.

Resume:

{resume_text}


Job Description:

{job_description}



Return ONLY JSON:


{{
"match_score":0,
"matching_skills":[],
"missing_skills":[],
"recommendations":[]
}}


Rules:

- Score 0-100 only.
- Junior projects count as experience.
- GitHub projects count.
- Python Django projects count.
- IT support counts as technical experience.
- Do not penalize junior candidates heavily.

"""



        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role":"user",
                    "content":prompt
                }

            ],

            temperature=0

        )



        data = clean_json_response(

            completion.choices[0].message.content

        )



        if "match_score" in data:


            try:


                score = float(
                    data["match_score"]
                )


                if score <= 1:

                    score *= 100



                score = max(
                    0,
                    min(
                        score,
                        100
                    )
                )



                data["match_score"] = int(
                    round(score)
                )



            except Exception:


                data["match_score"] = 0




        return Response(
            data
        )








# ======================================
# CAREER ASSISTANT
# ======================================


@extend_schema(

    request=AssistantSerializer,

    responses={
        200:dict
    }

)


@api_view(
    ["POST"]
)


@permission_classes(
    [IsAuthenticated]
)


def career_assistant(request):


    serializer = AssistantSerializer(
        data=request.data
    )



    serializer.is_valid(
        raise_exception=True
    )



    question = serializer.validated_data[
        "question"
    ]



    client = get_groq_client()



    completion = client.chat.completions.create(


        model="llama-3.3-70b-versatile",


        messages=[

            {
                "role":"user",
                "content":question
            }

        ],


        temperature=0.3

    )



    return Response(

        {

            "answer":
            completion.choices[0].message.content

        }

    )