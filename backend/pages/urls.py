from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
       path(
        "analyze/",
        views.analyze_job,
        name="analyze"
    ),


]