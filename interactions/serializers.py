from rest_framework import serializers
from .models import Interest, Match
from profiles.serializers import ProfileSerializer


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ("id", "to_profile", "created_at")

    def validate(self, data):
        request = self.context.get("request")
        if request and request.user.profile == data["to_profile"]:
            raise serializers.ValidationError(
                "Вы не можете выразить интерес к собственному профилю."
            )
        return data


class MatchSerializer(serializers.ModelSerializer):
    partner_profile = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ("id", "partner_profile", "created_at")

    def get_partner_profile(self, obj):
        request = self.context.get("request")
        current_profile = request.user.profile

        if obj.profile_one == current_profile:
            partner = obj.profile_two
        else:
            partner = obj.profile_one

        return ProfileSerializer(partner, context=self.context).data
