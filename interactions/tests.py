from django.contrib.auth import get_user_model
from django.test import TestCase
from profiles.models import Profile
from interactions.models import Interest, Match

User = get_user_model()


class MatchSignalTests(TestCase):

    def setUp(self):
        # Создаем двух пользователей для теста
        self.user_a = User.objects.create_user(
            email="user_a@test.com", password="password123"
        )
        self.user_b = User.objects.create_user(
            email="user_b@test.com", password="password123"
        )

        # Используем get_or_create: если сигнал уже создал профили,
        # мы их просто получим. Если нет — создадим вручную.
        self.profile_a, _ = Profile.objects.get_or_create(user=self.user_a)
        self.profile_b, _ = Profile.objects.get_or_create(user=self.user_b)

    def test_mutual_interest_creates_match_automatically(self):
        # Проверяем, что взаимный лайк автоматически генерирует матч

        # 1. Юзер А проявляет интерес к Юзеру Б
        interest_1 = Interest.objects.create(
            from_profile=self.profile_a, to_profile=self.profile_b
        )

        # Проверяем, что матча еще нет
        self.assertEqual(Match.objects.count(), 0)

        # 2. Юзер Б проявляет ответный интерес к Юзеру А
        interest_2 = Interest.objects.create(
            from_profile=self.profile_b, to_profile=self.profile_a
        )

        # Сигнал должен был сработать! Проверяем, что матч создался
        self.assertEqual(Match.objects.count(), 1)

        # Проверяем, что матч связывает именно этих двух пользователей
        match = Match.objects.first()
        self.assertTrue(
            (
                match.profile_one == self.profile_a
                and match.profile_two == self.profile_b
            )
            or (
                match.profile_one == self.profile_b
                and match.profile_two == self.profile_a
            )
        )
