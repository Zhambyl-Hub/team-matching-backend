from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Interest, Match


@receiver(post_save, sender=Interest)
def check_for_mutual_interest(sender, instance, created, **kwargs):
    if created:
        # instance - это только что созданный лайк (от А к Б)
        from_profile = instance.from_profile
        to_profile = instance.to_profile

        # Ищем, есть ли уже обратный лайк (от Б к А)
        reverse_interest_exists = Interest.objects.filter(
            from_profile=to_profile, to_profile=from_profile
        ).exists()

        if reverse_interest_exists:
            # Если обратный лайк есть - у нас взаимный матч
            # Что-бы избежать дубликатов, всегда сохраняем профили в определенном порядке
            # (например сначала тот у кого id меньше)
            p1, p2 = sorted([from_profile, to_profile], key=lambda p: p.id)

            # Создаем матч если его еще почему-то нет
            Match.objects.get_or_create(profile_one=p1, profile_two=p2)
