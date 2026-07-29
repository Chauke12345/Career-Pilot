from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Profile
from .serializers import ProfileSerializer


from docx import Document
import pdfplumber




# ==========================
# CV TEXT EXTRACTION
# ==========================

def extract_resume_text(file):

    text = ""

    try:

        filename = file.name.lower()


        if filename.endswith(".pdf"):

            with pdfplumber.open(file) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:

                        text += page_text + "\n"



        elif filename.endswith(".docx"):

            document = Document(file)


            for paragraph in document.paragraphs:

                text += paragraph.text + "\n"



    except Exception as e:

        print(
            "Resume extraction error:",
            e
        )


    return text.strip()





# ==========================
# PROFILE API
# ==========================

class ProfileView(APIView):


    permission_classes = [
        IsAuthenticated
    ]



    def get(self, request):


        profile, created = Profile.objects.get_or_create(
            user=request.user
        )


        serializer = ProfileSerializer(
            profile
        )


        return Response(
            serializer.data
        )




    def put(self, request):


        profile, created = Profile.objects.get_or_create(
            user=request.user
        )


        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )


        if serializer.is_valid():

            serializer.save()


            return Response(
                serializer.data
            )


        return Response(
            serializer.errors,
            status=400
        )





# ==========================
# UPLOAD CV
# ==========================


class UploadResumeView(APIView):


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



        profile, created = Profile.objects.get_or_create(
            user=request.user
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




        profile.resume = resume

        profile.resume_text = resume_text

        profile.save()



        return Response(
            {
                "message":
                "Resume uploaded successfully",

                "characters_extracted":
                len(resume_text)
            }
        )