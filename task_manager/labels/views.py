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
        self.object = self.get_object()

        # Проверяем, связана ли метка с задачами
        if self.object.tasks.exists():
            messages.error(
                request,
                'Невозможно удалить метку, потому что она используется'
            )
            return redirect(self.success_url)

        # Если не связана — удаляем
        messages.success(request, 'Метка успешно удалена')
        self.object.delete()
        return redirect(self.success_url)
