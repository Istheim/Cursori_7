
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from faker import Faker
from habit.models import Habit
from habit.serliazers import HabitSerializer
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.fake = Faker()
        self.user = User.objects.create(
            email='admin13@gmail.ru',
            password='admin13',
            is_superuser=True
        )
        self.client.force_authenticate(user=self.user)

    def create_fake_habit(self):
        return Habit.objects.create(
            user=self.user,
            place=self.fake.word(),
            timing=self.fake.time(),
            action=self.fake.word(),
            is_pleasurable=self.fake.boolean(),
            frequency=Habit.EVERY_DAY,
            reward=self.fake.sentence(),
            time_to_perform=self.fake.random_int(60, 120),
            is_public=self.fake.boolean()
        )

    def test_create_habit(self):
        user = self.user
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        data = {
            "user": user.pk,
            "place": self.fake.word(),
            "timing": self.fake.time(),
            "action": self.fake.word(),
            "is_pleasurable": self.fake.boolean(),
            "frequency": Habit.EVERY_DAY,
            "reward": None,
            "time_to_perform": self.fake.random_int(60, 120),
            "is_public": self.fake.boolean()
        }

        serializer = HabitSerializer(data=data)

        if serializer.is_valid():
            serializer.save()  # Сохранение объекта, если данные действительны
        else:
            errors = serializer.errors  # Обработка ошибок валидации
            print(errors)

        response = self.client.post(reverse("habit:habit-create"), data, format='json')
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_list_habit(self):
        user = self.user
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        # Создайте несколько случайных привычек
        for _ in range(5):
            self.create_fake_habit()

        response = self.client.get(reverse('habit:habit-list'))
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_update_habit(self):
        user = self.user
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        habit = self.create_fake_habit()
        data = {
            "place": self.fake.word(),
            "action": self.fake.word(),
        }

        response = self.client.patch(reverse('habit:habit-update', args=[habit.pk]), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.place, data["place"])
        self.assertEqual(habit.action, data["action"])

    def test_delete_habit(self):
        user = self.user
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        habit = self.create_fake_habit()
        response = self.client.delete(reverse('habit:habit-delete', args=[habit.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
