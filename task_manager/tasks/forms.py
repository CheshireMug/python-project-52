from django import forms
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "executor",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Имя"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Описание"
            }),
            "status": forms.Select(attrs={
                "class": "form-select",
            }),
            "executor": forms.Select(attrs={
                "class": "form-select",
            }),
        }

        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
        }
