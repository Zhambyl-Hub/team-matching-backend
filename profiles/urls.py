from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, InterestAreaViewSet, ProfileViewSet

router = DefaultRouter()
router.register("skills", SkillViewSet, basename="skill")
router.register("interests", InterestAreaViewSet, basename="interest")
router.register("profiles", ProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
]
