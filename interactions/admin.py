from django.contrib import admin
from .models import Interest, Match


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("id", "from_profile", "to_profile", "created_at")
    search_fields = ("from_profile__user__email", "to_profile__user__email")


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "profile_one", "profile_two", "created_at")
    search_fields = ("profile_one__user__email", "profile_two__user__email")
