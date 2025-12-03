from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create your tests here.
class UsersCRUDTest(TestCase):
    def setUp(self):
        # создаем пользователя в базе
        self.user = User.objects.create_user(
            username="john",
            first_name="John",
            last_name="Doe",
            password="12345"
        )

    def test_user_create(self):
        url = reverse('users:users_create')

        response = self.client.post(url, data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'username': 'janesmith',
            'password1': '12345',
            'password2': '12345',
        }, follow=True)

        # пользователь создан
        self.assertTrue(User.objects.filter(username='janesmith').exists())

        # редирект на login
        self.assertRedirects(response, reverse('login'))

        # флеш сообщение
        self.assertContains(response, 'Пользователь успешно зарегистрирован')

    def test_user_update(self):
        # логиним пользователя
        self.client.login(username='john', password='12345')

        url = reverse('users:users_update', kwargs={'pk': self.user.pk})

        response = self.client.post(url, data={
            'first_name': 'Joe',
            'last_name': 'Doe',
            'username': 'joe',
            'password1': '',
            'password2': '',
        }, follow=True)

        self.assertRedirects(response, reverse('users:users_list'))

        # обновление произошло
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Joe')

        # флеш сообщение
        self.assertContains(response, 'Данные пользователя обновлены')

    def test_user_delete(self):
        self.client.login(username='john', password='12345')

        url = reverse('users:users_delete', kwargs={'pk': self.user.pk})

        response = self.client.post(url, follow=True)

        # пользователь удалён
        self.assertFalse(User.objects.filter(username='john').exists())

        # редирект на список пользователей
        self.assertRedirects(response, reverse('users:users_list'))

        # флеш сообщение
        self.assertContains(response, 'Пользователь успешно удалён')
