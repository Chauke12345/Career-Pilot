from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile

        fields = [
            "full_name",
            "location",
            "linkedin",
            "github",
            "portfolio",
            "skills",
            "bio",
        ]