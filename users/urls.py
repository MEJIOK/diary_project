from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (GeneratePasswordView, RegisterView,
                         UserProfileUpdateView, UserProfileView, email_confirm,
                         login_view)

# Имя пространства имен для приложения "users"
app_name = UsersConfig.name

# URL-паттерны для управления пользовательскими функциями
urlpatterns = [
    # Страница входа пользователя
    path("login/", login_view, name="login"),
    # Страница выхода из системы
    path("logout/", LogoutView.as_view(), name="logout"),
    # Страница регистрации нового пользователя
    path("register/", RegisterView.as_view(), name="register"),
    # Подтверждение email через проверочный код
    path("email-confirm/<str:verification_code>/", email_confirm, name="email-confirm"),
    # Страница для генерации нового пароля
    path("reset/", GeneratePasswordView.as_view(), name="reset"),
    # Страница профиля пользователя
    path("profile/", UserProfileView.as_view(), name="profile"),
    # Страница для редактирования профиля пользователя
    path("profile/edit/", UserProfileUpdateView.as_view(), name="edit_profile"),
]
