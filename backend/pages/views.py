from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def login_page(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def dashboard(request):
    return render(request, "dashboard.html")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



@csrf_exempt
def analyze_job(request):

    if request.method == "POST":

        data = json.loads(request.body)

        job_description = data.get(
            "jobDescription",
            ""
        )


        # Temporary AI logic
        skills = [
            "Python",
            "Django",
            "JavaScript",
            "PostgreSQL"
        ]


        matches = []


        for skill in skills:

            if skill.lower() in job_description.lower():

                matches.append(skill)



        return JsonResponse({

            "match_percentage":
            len(matches) * 25,


            "matched_skills":
            matches,


            "message":
            "Analysis completed"

        })


    return JsonResponse({

        "error":"POST request required"

    })

from django.shortcuts import render

def applications(request):
    return render(request, "applications.html")