from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status

User = get_user_model()

# Create your tests here.
class LabelsCRUDTest(TestCase):

    def setUp(self):
        # Пользователь
        self.user = User.objects.create_user(
            username='user',
            password='test123'
        )

        # Статус нужен, чтобы создавать задачи
        self.status = Status.objects.create(name='TestStatus')

        # Метка
        self.label = Label.objects.create(name='TestLabel')

    # 1. Тест доступа
    def test_labels_list_requires_login(self):
        response = self.client.get(reverse('labels:labels_list'))
        self.assertEqual(response.status_code, 302)  # redirect to login

    # 2. Список меток
    def test_labels_list(self):
        self.client.login(username='user', password='test123')
        response = self.client.get(reverse('labels:labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestLabel')

    # 3. Создание метки
    def test_label_create(self):
        self.client.login(username='user', password='test123')

        response = self.client.post(
            reverse('labels:labels_create'),
            {'name': 'NewLabel'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='NewLabel').exists())

    # 4. Обновление метки
    def test_label_update(self):
        self.client.login(username='user', password='test123')

        response = self.client.post(
            reverse('labels:labels_update', args=[self.label.pk]),
            {'name': 'UpdatedLabel'}
        )

        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'UpdatedLabel')

    # 5. Удаление свободной метки
    def test_label_delete(self):
        self.client.login(username='user', password='test123')

        response = self.client.post(
            reverse('labels:labels_delete', args=[self.label.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    # 6. Запрет удаления метки, связанной с задачей
    def test_label_delete_protected(self):
        self.client.login(username='user', password='test123')

        # Создаём задачу с меткой
        task = Task.objects.create(
            name='Test task',
            status=self.status,
            author=self.user
        )
        task.labels.add(self.label)

        # Пытаемся удалить метку
        response = self.client.post(
            reverse('labels:labels_delete', args=[self.label.pk])
        )

        # Перенаправление на список
        self.assertEqual(response.status_code, 302)

        # Метка НЕ должна удалиться
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
