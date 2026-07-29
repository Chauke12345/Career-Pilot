from django.urls import path

from .views import (
    JobAnalyzerView,
    ResumeAnalyzerView,
    MatchResumeView,
    career_assistant
)


urlpatterns = [

    path(
        "analyze-job/",
        JobAnalyzerView.as_view(),
        name="analyze-job"
    ),


    path(
        "analyze-resume/",
        ResumeAnalyzerView.as_view(),
        name="analyze-resume"
    ),


    path(
        "match-resume/",
        MatchResumeView.as_view(),
        name="match-resume"
    ),


    path(
        "assistant/",
        career_assistant,
        name="career-assistant"
    ),

]