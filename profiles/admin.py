from django.contrib import admin
from .models import Skill, InterestArea, Profile


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(InterestArea)
class InterestAreaAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location", "stage", "is_approved", "created_at")
    list_filter = ("is_approved", "stage", "commitment", "location")
    search_fields = ("user__email", "bio")
    # Позволяет одобрять профили прямо из списка, не заходя внутрь каждого
    list_editable = ("is_approved",)
