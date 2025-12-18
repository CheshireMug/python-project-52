from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UsersCRUDTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(username="john")

    def test_user_create(self):
        url = reverse("users:users_create")

        response = self.client.post(
            url,
            data={
                "first_name": "Jane",
                "last_name": "Smith",
                "username": "janesmith",
                "password1": "12345",
                "password2": "12345",
            },
            follow=True,
        )

        self.assertTrue(User.objects.filter(username="janesmith").exists())
        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "Пользователь успешно зарегистрирован")

    def test_user_update(self):
        self.client.login(username="john", password="12345")

        url = reverse("users:users_update", kwargs={"pk": self.user.pk})

        response = self.client.post(
            url,
            data={
                "first_name": "Joe",
                "last_name": "Doe",
                "username": "joe",
                "password1": "",
                "password2": "",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("users:users_list"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Joe")
        self.assertContains(response, "Пользователь успешно изменен")

    def test_user_delete(self):
        self.client.login(username="john", password="12345")

        url = reverse("users:users_delete", kwargs={"pk": self.user.pk})

        response = self.client.post(url, follow=True)

        self.assertFalse(User.objects.filter(username="john").exists())
        self.assertRedirects(response, reverse("users:users_list"))
        self.assertContains(response, "Пользователь успешно удалён")
