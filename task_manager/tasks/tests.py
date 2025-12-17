from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class TasksFilterTest(TestCase):
    fixtures = [
        "users.json",
        "statuses.json",
        "labels.json",
        "tasks.json",
        "task_labels.json",
    ]

    def setUp(self):
        self.user1 = User.objects.get(username="user1")
        self.user2 = User.objects.get(username="user2")

        self.status1 = Status.objects.get(name="StatusA")
        self.label1 = Label.objects.get(name="LabelA")

        self.list_url = reverse("tasks:tasks_list")

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
