from django.urls import path

from .views import (
    JobAnalyzerView,
    career_assistant
)


urlpatterns = [

    path(
        "analyze-job/",
        JobAnalyzerView.as_view(),
        name="analyze-job"
    ),


    path(
        "assistant/",
        career_assistant,
        name="career-assistant"
    ),

]