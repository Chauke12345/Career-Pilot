from django.urls import path

from .views import ResumeMatchView



urlpatterns = [

    path(
        "analyze/",
        ResumeMatchView.as_view(),
        name="resume-match"
    ),

]