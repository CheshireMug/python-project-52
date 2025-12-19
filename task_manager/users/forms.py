from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm
from django import forms
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        }),
        label='Имя пользователя'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        label='Пароль'
    )


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
            'required': True,
        })
    )

    last_name = forms.CharField(
        max_length=150,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия',
            'required': True,
        })
    )

    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'required': True,
            'autofocus': True,
        }),
        help_text='Обязательное поле. Не более 150 символов. '
                  'Только буквы, цифры и символы @/./+/-/_.'
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        }),
        help_text='<ul><li>Ваш пароль должен содержать' + \
        ' как минимум 3 символа.</li></ul>'
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
        }),
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2"
            ]


class UserUpdateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
            'required': True,
        })
    )

    last_name = forms.CharField(
        max_length=150,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия',
            'required': True,
        })
    )

    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'required': True,
            'autofocus': True,
        }),
        help_text='Обязательное поле. Не более 150 символов. '
                  'Только буквы, цифры и символы @/./+/-/_.'
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        }),
        required=False,
        help_text='<ul><li>Ваш пароль должен содержать' + \
            ' как минимум 3 символа.</li></ul>'
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
        }),
        required=False,
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
            ]
