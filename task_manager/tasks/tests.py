from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()

# Create your tests here.
class TasksFilterTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="pass123",
            first_name="User", last_name="One"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="pass123",
            first_name="User", last_name="Two"
        )

        self.status1 = Status.objects.create(name="StatusA")
        self.status2 = Status.objects.create(name="StatusB")

        self.label1 = Label.objects.create(name="LabelA")
        self.label2 = Label.objects.create(name="LabelB")

        self.task1 = Task.objects.create(
            name="Task 1",
            status=self.status1,
            author=self.user1,
            executor=self.user1
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name="Task 2",
            status=self.status2,
            author=self.user2,
            executor=self.user2
        )
        self.task2.labels.add(self.label2)

        self.list_url = reverse("tasks:tasks_list")

    # ТЕСТЫ ФИЛЬТРАЦИИ

    def test_filter_by_status(self):
        response = self.client.get(self.list_url, {"status": self.status1.id})
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_filter_by_executor(self):
        response = self.client.get(self.list_url, {"executor": self.user2.id})
        self.assertContains(response, "Task 2")
        self.assertNotContains(response, "Task 1")

    def test_filter_by_label(self):
        response = self.client.get(self.list_url, {"label": self.label1.id})
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_filter_only_self_tasks(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.get(self.list_url, {"self_tasks": "on"})
        self.assertContains(response, "Task 1")
        self.assertNotContains(response, "Task 2")

    def test_no_filters_show_all(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Task 2")
