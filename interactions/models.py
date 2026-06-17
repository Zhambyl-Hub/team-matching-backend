from django.db import models
from profiles.models import Profile


class Interest(models.Model):
    # Модель проявления интереса (лайк)
    from_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="sent_interests"
    )
    to_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="received_interests"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Уникальный индекс, чтобы нельзя было лайкнуть одного человека дважды
        unique_together = ("from_profile", "to_profile")

    def __str__(self):
        return f"{self.from_profile.user.email} -> {self.to_profile.user.email}"


class Match(models.Model):
    # Модель взаимного соответствия (Матч)
    profile_one = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="matches_as_one"
    )
    profile_two = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="matches_as_two"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile_one", "profile_two")

    def __str__(self):
        return f"{self.profile_one.user.email} -> {self.profile_two.user.email}"
