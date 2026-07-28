from rest_framework import serializers


class MatchSerializer(serializers.Serializer):

    resume = serializers.FileField()

    job_description = serializers.CharField(
        min_length=50
    )