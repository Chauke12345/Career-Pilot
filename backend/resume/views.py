from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Resume
from .serializers import ResumeSerializer
from .services import (
    extract_resume_text,
    analyze_resume,
)

class ResumeAnalyzerView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ResumeSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        resume = serializer.save(
            user=request.user
        )

        text = extract_resume_text(
            resume.resume
        )

        analysis = analyze_resume(
            text
        )

        resume.analysis = analysis

        resume.save()

        return Response(analysis)