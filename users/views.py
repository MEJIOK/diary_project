import secrets

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import (CustomPasswordResetForm, UserLoginForm,
                         UserProfileForm, UserRegisterForm)
from users.models import User


def login_view(request):
    """
    Представление для входа пользователя в систему.

    Если форма входа валидна, выполняется аутентификация пользователя на основе
    введенных данных (email и пароль). В случае успешного входа пользователя
    перенаправляет на список записей в дневнике.

    Аргументы:
        request (HttpRequest): Запрос на вход пользователя.

    Возвращает:
        HttpResponse: Если данные введены корректно, происходит перенаправление на страницу дневника.
        В противном случае отображается форма входа с сообщением об ошибке.
    """

    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("diary:list")
    return render(
        request, "users/login.html", {"form": form, "title": "Войти в аккаунт"}
    )


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.

    Пользователь создается как неактивный, и ему отправляется email с кодом подтверждения.
    После подтверждения email аккаунт становится активным.
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """
        Обрабатывает сохранение формы, создавая неактивного пользователя и отправляя код подтверждения на почту.

        Аргументы:
            form (UserRegisterForm): Форма регистрации пользователя.

        Возвращает:
            HttpResponse: Перенаправляет на страницу входа после успешной регистрации.
        """
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data["password1"])
        verification_code = secrets.token_hex(16)
        user.verification_code = verification_code
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{verification_code}"

        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения почты перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Добавляет заголовок страницы в контекст.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context


def email_confirm(request, verification_code):
    """
    Подтверждение email пользователя через код верификации.

    Если код подтверждения верен, аккаунт пользователя активируется.

    Аргументы:
        request (HttpRequest): Запрос на подтверждение email.
        verification_code (str): Код подтверждения, переданный через URL.

    Возвращает:
        HttpResponse: Перенаправляет на страницу входа после успешного подтверждения email.
    """
    user = get_object_or_404(User, verification_code=verification_code)
    if user.is_active:
        messages.info(request, "Аккаунт уже активирован.")
    else:
        user.is_active = True
        user.verification_code = None
        user.save()
        return redirect("users:login")


class UserProfileView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения профиля пользователя.

    Это представление требует, чтобы пользователь был авторизован.
    Отображает информацию о текущем пользователе.
    """

    model = User
    template_name = "users/profile.html"

    def get_object(self, **kwargs):
        """
        Возвращает текущего авторизованного пользователя.
        """
        return self.request.user


class GeneratePasswordView(PasswordResetView):
    """
    Представление для генерации нового пароля.

    Пользователь вводит свой email, после чего на него отправляется новый сгенерированный пароль.
    """

    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("users:login")
    template_name = "users/reset_password.html"

    def form_valid(self, form):
        """
        Обрабатывает запрос на генерацию нового пароля.

        Проверяет, существует ли пользователь с указанным email, генерирует новый пароль
        и отправляет его пользователю на email.
        """
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            password = User.objects.make_random_password(length=8)
            user.set_password(password)
            user.save()

            send_mail(
                "Смена пароля",
                f"Здравствуйте. Вы запросили генерацию нового пароля для сайта. "
                f"Ваш новый пароль: {password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except User.DoesNotExist:
            messages.error(self.request, "Пользователь с таким email не найден.")
            return super().form_invalid(form)

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        """
        Добавляет заголовок страницы в контекст.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Восстановление пароля"
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля пользователя.

    Пользователь может редактировать только свой профиль.
    """

    model = User
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, **kwargs):
        """
        Возвращает текущего авторизованного пользователя для редактирования.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Добавляет заголовок страницы в контекст.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование профиля"
        return context
