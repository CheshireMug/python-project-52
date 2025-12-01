from django.contrib import messages
from django.views.generic import ListView, CreateView,\
    UpdateView, DeleteView
from .models import Task
from django.http import HttpResponse
from .models import Task
from .forms import TaskCreateForm
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Create your views here.
class TasksListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/index.html'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:tasks_list')

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена')
        return super().form_valid(form)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:tasks_list')

    def post(self, request, *args, **kwargs):
        # получаем объект
        self.object = self.get_object()

        # сообщение ДО удаления
        messages.success(request, 'Задача успешно удалена')

        # удаляем статус
        self.object.delete()

        # редирект
        return redirect(self.success_url)
