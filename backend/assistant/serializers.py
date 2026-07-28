from rest_framework import serializers


class AssistantSerializer(serializers.Serializer):

    question = serializers.CharField()