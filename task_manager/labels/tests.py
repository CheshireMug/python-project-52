from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label

User = get_user_model()


class LabelsCRUDTest(TestCase):
    fixtures = [
        "users.json",
        "statuses.json",
        "labels.json",
        "tasks.json",
        "task_labels.json",
    ]

    def setUp(self):
        self.user = User.objects.get(username="user")
        self.label = Label.objects.get(name="TestLabel")

    # Тест доступа
    def test_labels_list_requires_login(self):
        response = self.client.get(reverse("labels:labels_list"))
        self.assertEqual(response.status_code, 302)

    # Список меток
    def test_labels_list(self):
        self.client.login(username="user", password="test123")
        response = self.client.get(reverse("labels:labels_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestLabel")

    # Создание метки
    def test_label_create(self):
        self.client.login(username="user", password="test123")

        response = self.client.post(
            reverse("labels:labels_create"),
            {"name": "NewLabel"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name="NewLabel").exists())

    # Обновление метки
    def test_label_update(self):
        self.client.login(username="user", password="test123")

        response = self.client.post(
            reverse("labels:labels_update", args=[self.label.pk]),
            {"name": "UpdatedLabel"},
        )

        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "UpdatedLabel")

    # Удаление свободной метки
    def test_label_delete(self):
        self.client.login(username="user", password="test123")

        free_label = Label.objects.get(name="FreeLabel")

        response = self.client.post(
            reverse("labels:labels_delete", args=[free_label.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=free_label.pk).exists())

    # Запрет удаления метки, связанной с задачей
    def test_label_delete_protected(self):
        self.client.login(username="user", password="test123")

        response = self.client.post(
            reverse("labels:labels_delete", args=[self.label.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
