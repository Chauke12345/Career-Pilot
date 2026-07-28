from django.urls import path

from .views import (
    JobApplicationListCreateView,
    JobApplicationDetailView,
    ApplicationEventListCreateView,
)


urlpatterns = [

    # List + Create applications
    path(
        "",
        JobApplicationListCreateView.as_view(),
        name="applications"
    ),


    # Retrieve + Update + Delete application
    path(
        "<int:pk>/",
        JobApplicationDetailView.as_view(),
        name="application-detail"
    ),


    # Application events
    path(
        "<int:application_id>/events/",
        ApplicationEventListCreateView.as_view(),
        name="application-events"
    ),

]