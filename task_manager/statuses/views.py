from django.contrib import messages
from django.views.generic import ListView, CreateView,\
    UpdateView, DeleteView
from .models import Status
from .forms import StatusCreateForm
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Create your views here.
class StatusesListView(ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/index.html'


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Статус успешно создан'
            )
        return super().form_valid(form)


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменен')
        return super().form_valid(form)


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def post(self, request, *args, **kwargs):
        # получаем объект
        self.object = self.get_object()

        # сообщение ДО удаления
        messages.success(request, 'Статус успешно удален')

        # удаляем статус
        self.object.delete()

        # редирект
        return redirect(self.success_url)
