from rest_framework import serializers


class JobAnalyzerSerializer(serializers.Serializer):

    job_description = serializers.CharField(
        required=True,
        min_length=50
    )


class AssistantSerializer(serializers.Serializer):

    question = serializers.CharField(
        required=True,
        min_length=5
    )


class ResumeUploadSerializer(serializers.Serializer):

    resume = serializers.FileField(
        required=True
    )

    job_description = serializers.CharField(
        required=True,
        min_length=50
    )