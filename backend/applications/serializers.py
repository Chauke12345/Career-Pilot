from rest_framework import serializers
from .models import JobApplication, ApplicationEvent


class ApplicationEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationEvent
        fields = [
            "id",
            "title",
            "date",
            "notes",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class JobApplicationSerializer(serializers.ModelSerializer):

    events = ApplicationEventSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = JobApplication

        fields = [
            "id",
            "company",
            "position",
            "location",
            "status",
            "job_link",
            "notes",
            "date_applied",
            "created_at",
            "events",
        ]

        read_only_fields = [
            "id",
            "date_applied",
            "created_at",
        ]