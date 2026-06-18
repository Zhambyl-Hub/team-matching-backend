from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    # Кастомный менеджер, где email является уникальным идентификатором

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)

        # По умолчанию для обычного пользователя ставим username в None,
        # если он не передан явно
        extra_fields.setdefault("username", None)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        # Для суперпользователя в панели Django Admin поле username желательно,
        # поэтому автоматически генерируем его из первой части email, если оно пустое
        if not extra_fields.get("username"):
            extra_fields["username"] = email.split("@")[0]

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        _("username"), max_length=150, unique=True, blank=True, null=True
    )
    email = models.EmailField(_("email address"), unique=True)

    # Подключаем наш кастомный менеджер
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Убираем username из обязательных полей CLI-команд

    def __str__(self):
        return self.email
