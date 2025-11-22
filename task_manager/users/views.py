from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,\
    UserPassesTestMixin
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from .forms import RegistrationForm
from django.views.generic import ListView, CreateView,\
    UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import UserUpdateForm
from .models import User

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
            'Пользователь успешно зарегистрирован. Войдите, пожалуйста.'
            )
        return super().form_valid(form)


class UserIsSelfMixin(UserPassesTestMixin):

    def test_func(self):
        # obj = self.get_object()
        # return self.request.user.is_authenticated and obj.pk == self.request.user.pk
        try:
            obj = self.get_object()
        except User.DoesNotExist:
            return False
        return self.request.user.is_authenticated and \
            obj.pk == self.request.user.pk

    def handle_no_permission(self):
        # # Если не авторизован отправляем на логин
        # if not self.request.user.is_authenticated:
        #     messages.error(
        #         self.request,
        #         'Вы не авторизованы! Пожалуйста, выполните вход.'
        #         )
        #     return redirect(reverse_lazy('login'))

        # # Если авторизован, но не свой профиль возвращаем на список пользователей
        # messages.error(self.request, 'У вас нет прав для изменения этого пользователя.')
        # return redirect(reverse_lazy('users:users_list'))
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse_lazy('login'))

        # Если объект уже не существует — после delete() — не ломаем редирект
        messages.error(self.request, 'У вас нет прав для изменения этого пользователя.')
        return redirect(reverse_lazy('users:users_list'))


class UserUpdateView(LoginRequiredMixin, UserIsSelfMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:users_list')

    def form_valid(self, form):
        messages.success(self.request, 'Данные пользователя обновлены.')
        return super().form_valid(form)


# class UserDeleteView(LoginRequiredMixin, UserIsSelfMixin, DeleteView):
#     model = User
#     template_name = 'users/delete.html'
#     success_url = reverse_lazy('users:users_list')

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, 'Пользователь успешно удалён.')
#         return super().delete(request, *args, **kwargs)

class UserDeleteView(LoginRequiredMixin, UserIsSelfMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:users_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Пользователь успешно удалён.')
        logout(request)
        return super().delete(request, *args, **kwargs)
