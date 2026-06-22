from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Interest, Match
from .serializers import InterestSerializer, MatchSerializer


class InteractionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="like")
    def like_profile(self, request):
        serializer = InterestSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        from_profile = request.user.profile
        to_profile = serializer.validated_data["to_profile"]

        if Interest.objects.filter(
            from_profile=from_profile, to_profile=to_profile
        ).exists():
            return Response(
                {"detail": "Вы уже выразили интерес к этому пользователю."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(from_profile=from_profile)

        is_match = Match.objects.filter(
            (Q(profile_one=from_profile) & Q(profile_two=to_profile))
            | (Q(profile_one=to_profile) & Q(profile_two=from_profile))
        ).exists()

        return Response(
            {"message": "Интерес успешно зафиксирован", "is_match": is_match},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["get"], url_path="matches")
    def my_matches(self, request):
        profile = request.user.profile
        matches = Match.objects.filter(Q(profile_one=profile) | Q(profile_two=profile))

        serializer = MatchSerializer(matches, many=True, context={"request": request})
        return Response(serializer.data)
