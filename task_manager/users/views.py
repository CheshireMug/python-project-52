from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,\
    UserPassesTestMixin
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView,\
    UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import UserUpdateForm
from .models import User


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы залогинены")
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)


# Create your views here.
class UsersListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/index.html'


class UserCreateView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Пользователь успешно зарегистрирован'
            )
        return super().form_valid(form)


class UserIsSelfMixin(UserPassesTestMixin):

    def test_func(self):
        try:
            obj = self.get_object()
        except User.DoesNotExist:
            return False
        return self.request.user.is_authenticated and \
            obj.pk == self.request.user.pk

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse_lazy('login'))

        messages.error(self.request, 'У вас нет прав для изменения этого пользователя.')
        return redirect(reverse_lazy('users:users_list'))


class UserUpdateView(LoginRequiredMixin, UserIsSelfMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:users_list')

    def form_valid(self, form):
        messages.success(self.request, 'Данные пользователя обновлены')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserIsSelfMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:users_list')

    def post(self, request, *args, **kwargs):
        # получаем объект
        self.object = self.get_object()

        # сообщение ДО удаления
        messages.success(request, 'Пользователь успешно удалён')

        # логаут ДО удаления
        logout(request)

        # удаляем пользователя
        self.object.delete()

        # редирект
        return redirect(self.success_url)
