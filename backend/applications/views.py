from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import JobApplication, ApplicationEvent
from .serializers import (
    JobApplicationSerializer,
    ApplicationEventSerializer,
)


class JobApplicationListCreateView(generics.ListCreateAPIView):

    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = [
        "status",
    ]

    search_fields = [
        "company",
        "position",
        "location",
    ]


    def get_queryset(self):

        return JobApplication.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )



class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return JobApplication.objects.filter(
            user=self.request.user
        )
    



class ApplicationEventListCreateView(generics.ListCreateAPIView):

    serializer_class = ApplicationEventSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return ApplicationEvent.objects.filter(
            application__user=self.request.user,
            application_id=self.kwargs["application_id"]
        ).order_by("date")


    def perform_create(self, serializer):

        application = JobApplication.objects.get(
            id=self.kwargs["application_id"],
            user=self.request.user
        )

        serializer.save(
            application=application
        )