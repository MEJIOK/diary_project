from django.db import models
from django.contrib.auth.models import AbstractUser

# Определение NULLABLE для полей, которые могут быть пустыми или NULL
NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Кастомная модель пользователя, основанная на Django AbstractUser.

    В этой модели мы используем email в качестве основного поля для аутентификации,
    добавляем дополнительные поля, такие как аватар, телефон, страна и код верификации.

    Поля модели:
        - email: Уникальный адрес электронной почты для пользователя (используется для логина).
        - avatar: Изображение для профиля пользователя.
        - num_phone: Номер телефона пользователя.
        - country: Страна проживания пользователя.
        - verification_code: Код подтверждения (например, для подтверждения регистрации или восстановления пароля).
    """

    # Переопределение поля username
    username = "Не указано"  # Значение по умолчанию для имени пользователя

    # Email является уникальным и используется как основное поле для логина
    email = models.EmailField(unique=True, max_length=35, verbose_name="почта")

    # Аватар пользователя
    avatar = models.ImageField(
        upload_to="media/users/avatars", verbose_name="аватар", **NULLABLE
    )

    # Номер телефона пользователя
    num_phone = models.CharField(
        max_length=35, default="Не указано", verbose_name="телефон", **NULLABLE
    )

    # Страна проживания пользователя
    country = models.CharField(
        max_length=50, default="Не указано", verbose_name="страна", **NULLABLE
    )

    # Код подтверждения (например, для подтверждения email)
    verification_code = models.CharField(
        max_length=100, verbose_name="код подтверждения", **NULLABLE
    )

    # Используем email в качестве поля для аутентификации
    USERNAME_FIELD = "email"

    # Дополнительные обязательные поля для создания пользователя через командную строку или админку
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Возвращает строковое представление пользователя.
        Пример: "email пользователя - активен: True/False"
        """
        return f"{self.email} - активен:{self.is_active}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
