from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes

from drf_spectacular.utils import extend_schema

from .serializers import (
    JobAnalyzerSerializer,
    AssistantSerializer
)

from .services import analyze_job_description


import os
from groq import Groq





class JobAnalyzerView(APIView):

    permission_classes = [IsAuthenticated]


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


        print("JOB RECEIVED:")
        print(job_description)


        result = analyze_job_description(
            job_description
        )


        return Response(result)








@extend_schema(
    request=AssistantSerializer,
    responses={
        200: dict
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
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



    api_key = os.environ.get(
        "GROQ_API_KEY"
    )


    if not api_key:

        return Response(
            {
                "error": "Groq API key missing"
            },
            status=500
        )



    client = Groq(
        api_key=api_key
    )



    prompt = f"""
You are Career Pilot AI Assistant.

Help a junior software developer with:

- career advice
- CV improvement
- interview preparation
- learning roadmaps
- job searching strategies

User question:

{question}

Provide practical and actionable advice.
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

            temperature=0.3

        )


        return Response(
            {
                "answer":
                completion.choices[0].message.content
            }
        )


    except Exception as e:

        return Response(
            {
                "error": str(e)
            },
            status=500
        )