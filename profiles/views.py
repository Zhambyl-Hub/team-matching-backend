from django.db.models import Count, Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from interactions.models import Interest
from .models import InterestArea, Profile, Skill
from .serializers import InterestAreaSerializer, ProfileSerializer, SkillSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]


class InterestAreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InterestArea.objects.all()
    serializer_class = InterestAreaSerializer
    permission_classes = [permissions.AllowAny]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(is_approved=True)
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)

        if request.method == "GET":
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        elif request.method in ["PUT", "PATCH"]:
            partial = request.method == "PATCH"
            serializer = self.get_serializer(
                profile, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def recommendations(self, request):
        current_profile = request.user.profile

        already_liked_ids = Interest.objects.filter(
            from_profile=current_profile
        ).values_list("to_profile_id", flat=True)

        candidates = (
            Profile.objects.filter(is_approved=True)
            .exclude(id=current_profile.id)
            .exclude(id__in=already_liked_ids)
        )

        user_wants_skills = current_profile.skills_want.all()

        candidates = candidates.annotate(
            match_count=Count(
                "skills_have", filter=Q(skills_have__in=user_wants_skills)
            )
        ).order_by("-match_count", "-created_at")

        page = self.paginate_queryset(candidates)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(candidates, many=True)
        return Response(serializer.data)
