from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ResumeSerializer
from .services import (
    extract_resume_text,
    analyze_resume,
)


class ResumeAnalyzerView(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):

        try:


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



            return Response(
                analysis,
                status=status.HTTP_200_OK
            )


        except Exception as e:


            print(
                "RESUME VIEW ERROR:",
                str(e)
            )


            return Response(

                {
                    "error": str(e)
                },

                status=status.HTTP_500_INTERNAL_SERVER_ERROR

            )