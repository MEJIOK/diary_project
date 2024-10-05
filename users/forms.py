from django.contrib.auth import authenticate
from django import forms
from django.core.exceptions import ValidationError
from users.models import User


class UserLoginForm(forms.Form):
    """
    Форма для входа пользователя в систему.

    Поля формы:
        - email: Адрес электронной почты пользователя.
        - password: Пароль пользователя.

    Виджеты:
        - Настраиваемые классы для улучшения внешнего вида полей формы (Bootstrap).

    Методы:
        - clean: Проверяет правильность введенных данных и выполняет аутентификацию пользователя.
    """

    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean(self):
        """
        Проверяет, существует ли пользователь с указанным email и паролем.

        Выполняет аутентификацию пользователя с помощью метода authenticate.
        Если пользователь с указанными данными не существует, поднимается ValidationError.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            raise ValidationError("Неверный email или пароль")
        return cleaned_data


class UserRegisterForm(forms.ModelForm):
    """
    Форма для регистрации нового пользователя.

    Поля формы:
        - email: Адрес электронной почты пользователя.
        - password1: Пароль пользователя.
        - password2: Подтверждение пароля.

    Виджеты:
        - Настраиваемые классы для улучшения внешнего вида полей формы (Bootstrap).

    Методы:
        - clean_password: Проверяет, совпадают ли введенные пароли.
    """

    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_password(self):
        """
        Проверяет, совпадают ли введенные пароли.

        Если пароли не совпадают, поднимается ValidationError.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    class Meta:
        model = User
        fields = ["email"]


class CustomPasswordResetForm(forms.Form):
    """
    Форма для восстановления пароля пользователя по электронной почте.

    Поля формы:
        - email: Адрес электронной почты пользователя для отправки ссылки на восстановление пароля.

    Виджеты:
        - Настраиваемые классы для улучшения внешнего вида поля формы (Bootstrap).
    """

    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["email"]


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.

    Поля формы:
        - first_name: Имя пользователя.
        - last_name: Фамилия пользователя.
        - email: Адрес электронной почты.
        - num_phone: Номер телефона пользователя.
        - country: Страна пользователя.
        - avatar: Аватар пользователя.

    Виджеты:
        - Настраиваемые классы для улучшения внешнего вида полей формы (Bootstrap).
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "num_phone", "country", "avatar"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "num_phone": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
