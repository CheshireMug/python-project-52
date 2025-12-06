from django import forms
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label

class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label="Статус"
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Исполнитель"
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label="Метка"
    )
    self_tasks = forms.BooleanField(
        required=False,
        label="Только свои задачи"
    )
