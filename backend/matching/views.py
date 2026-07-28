from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import MatchSerializer

from resume.services import extract_resume_text
from .services import analyze_match



class ResumeMatchView(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):

        serializer = MatchSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        resume_file = serializer.validated_data[
            "resume"
        ]


        job_description = serializer.validated_data[
            "job_description"
        ]


        resume_text = extract_resume_text(
            resume_file
        )


        result = analyze_match(
            resume_text,
            job_description
        )


        return Response(result)