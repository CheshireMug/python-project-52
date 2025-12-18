from django.contrib import messages
from django.views.generic import ListView, CreateView,\
    UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Task
from django.http import HttpResponse
from .models import Task
from .forms import TaskCreateForm
from .filters import TaskFilterForm
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Create your views here.
class TasksListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["executors"] = User.objects.all()
        context["labels"] = Label.objects.all()   
        context["form"] = TaskFilterForm(self.request.GET or None)
        context["form_active"] = bool(self.request.GET)
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        # читать параметры из request.GET
        status = self.request.GET.get("status")
        executor = self.request.GET.get("executor")
        label = self.request.GET.get("label")
        self_tasks = self.request.GET.get("self_tasks")

        if status:
            qs = qs.filter(status=status)

        if executor:
            qs = qs.filter(executor=executor)

        if label:
            qs = qs.filter(labels=label)

        if self_tasks:
            qs = qs.filter(author=self.request.user)

        return qs


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/detail.html'


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
    # template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:tasks_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Задача успешно удалена')
        self.object.delete()
        return redirect(self.success_url)
    # def post(self, request, *args, **kwargs):
    #     # получаем объект
    #     self.object = self.get_object()

    #     # сообщение ДО удаления
    #     messages.success(request, 'Задача успешно удалена')

    #     # удаляем задачу
    #     self.object.delete()

    #     # редирект
    #     return redirect(self.success_url)
