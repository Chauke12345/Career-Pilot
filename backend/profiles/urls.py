from django.urls import path

from .views import (
    ProfileView,
    UploadResumeView
)


urlpatterns = [

    path(
        "",
        ProfileView.as_view(),
        name="profile"
    ),


    path(
        "upload-resume/",
        UploadResumeView.as_view(),
        name="upload-resume"
    ),

]