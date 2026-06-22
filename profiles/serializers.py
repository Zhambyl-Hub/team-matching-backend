from rest_framework import serializers
from .models import Skill, InterestArea, Profile


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("id", "name")


class InterestAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestArea
        fields = ("id", "name")


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "email",
            "bio",
            "portfolio_url",
            "github_url",
            "telegram_username",
            "stage",
            "commitment",
            "location",
            "skills_have",
            "skills_want",
            "interests",
            "is_approved",
        )

        read_only_fields = ("is_approved",)
