from django.urls import path
from .views import career_assistant


urlpatterns = [

    path(
        "",
        career_assistant,
        name="career-assistant"
    ),

]