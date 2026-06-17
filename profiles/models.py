from django.db import models
from django.conf import settings

from accounts.models import User


class Skill(models.Model):
    # Справочник навыков (например: python, react)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class InterestArea(models.Model):
    # Справочник сфер бизнеса (например: FinTech, EdTech)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    # Профиль пользователя, расширяющий базовую модель User
    class ProjectStage(models.TextChoices):
        IDEA = ("idea", "Есть только идея")
        PROTOTYPE = ("prototype", "Прототип / MVP")
        TRACTION = ("traction", "Есть пользователи / первые продажи")
        BUSINESS = ("business", "Работающий бизнес")
        LOOKING = ("looking", "Пока просто ищу проект")

    class CommitmentLevel(models.TextChoices):
        HOBBY = ("hobby", "Хобби (несколько часов в неделю)")
        PART_TIME = ("part_time", "Part-time (20 часов в неделю)")
        FULL_TIME = ("full_time", "Full-time (40+ часов в неделю)")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="Краткое био")

    # Ссылки на соцсети/портфолио
    portfolio_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    telegram_username = models.CharField(
        max_length=100, blank=True, help_text="Скрыто до взаимного матча"
    )
    # Выборы из списков (Choices)
    stage = models.CharField(
        max_length=20, choices=ProjectStage.choices, default=ProjectStage.LOOKING
    )
    commitment = models.CharField(
        max_length=20, choices=CommitmentLevel.choices, default=CommitmentLevel.HOBBY
    )
    location = models.CharField(max_length=100, default="Не указан")

    # Связи ManyToMany к справочникам
    skills_have = models.ManyToManyField(
        Skill, related_name="profiles_with_skill", blank=True
    )
    skills_want = models.ManyToManyField(
        Skill, related_name="profiles_seeking_skill", blank=True
    )
    interests = models.ManyToManyField(
        InterestArea, related_name="profiles_interested", blank=True
    )

    # Модерация для закрытого комьюнити
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Профиль: {self.user.user.email}"
