from django.contrib import messages
from django.views.generic import ListView, CreateView,\
    UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Label
from .forms import LabelCreateForm
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Create your views here.
class LabelsListView(LoginRequiredMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/index.html'
    login_url = 'login'


class LableCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:labels_list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(
            self.request,
            'Метка успешно создана'
            )
        return super().form_valid(form)


class LableUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:labels_list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Метка успешно изменена')
        return super().form_valid(form)


class LableDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:labels_list')
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        # получаем объект
        self.object = self.get_object()

        # сообщение ДО удаления
        messages.success(request, 'Метка успешно удалена')

        # удаляем статус
        self.object.delete()

        # редирект
        return redirect(self.success_url)
