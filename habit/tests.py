from builtins import list

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='admin13@gmail.ru',
            password='admin13',
            is_superuser=True
        )
        self.client.force_authenticate(user=self.user)

        # Создаем объект related_habit с именем 'drink water'
        self.related_habit = Habit.objects.create(
            user=self.user,
            place='Home',
            timing='7:00',
            action='drink water',
            is_pleasurable=True,
            frequency='Ежедневная',
            time_to_perform=90,
            is_public=True
        )

    def test_create_Habit(self):
        data = {
            "user": self.user.pk,
            "place": 'street',
            "timing": '8:00',
            "action": 'running',
            "is_pleasurable": True,
            "related_habit": self.related_habit.pk,
            "frequency": 'Ежедневная',
            "reward": None,
            "time_to_perform": 120,
            "is_public": True
        }

        response = self.client.post(reverse("habit:habit-create"), data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Habit.objects.count(), 2
        )

    def test_habit_list(self):
        response = self.client.get(
            reverse('habit:habit-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_update(self):
        data = {
            "user": self.user.pk,
            "place": 'зал',
            "timing": '10:00',
            "action": 'заниматься',
            "is_pleasurable": True,
            "related_habit": None,
            "frequency": 'Трехдневная',
            "reward": 'съесть сладкое',
            "time_to_perform": 100,
            "is_public": False
        }

        response = self.client.patch(
            reverse('habit:habit-update', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_destroy(self):
        response = self.client.delete(
            reverse('habit:habit-delete', kwargs={'pk': self.habit.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            list(Habit.objects.all()),
            []
        )

    def tearDown(self):
        self.user.delete()
        self.habit.delete()
