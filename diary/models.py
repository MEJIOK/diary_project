from django.db import models
from pytils.translit import slugify  # Модуль для транслитерации заголовков в slug
from django.conf import settings

# Свойства NULLABLE, которые можно определить в отдельном файле constants.py
NULLABLE = {"blank": True, "null": True}


class Diary(models.Model):
    """
    Модель для хранения записей в дневнике.

    Модель поддерживает различные состояния записей, такие как "Опубликовано",
    "На модерации", "Отклонено" и т. д. Она также позволяет учитывать количество просмотров,
    хранить изображение для каждой записи, а также автоматически генерировать уникальный slug на основе заголовка.

    Поля модели:
        - title: Заголовок записи.
        - content: Описание или основное содержание записи.
        - slug: Уникальный slug (URL-адрес) для записи, создается автоматически на основе заголовка.
        - author: Автор записи (ссылка на пользователя).
        - is_published: Логический флаг, который указывает, опубликована запись или нет.
        - status: Статус записи (например, "на модерации" или "опубликовано").
        - preview: Изображение для предварительного просмотра записи.
        - created_at: Дата создания записи.
        - views: Количество просмотров записи.
    """

    # Определение статусов записи (например, опубликовано, на модерации и т.д.)
    STATUS_CHOICES = (
        ("published", "Опубликовано"),
        ("no_published", "Не опубликовано"),
        ("moderation", "На модерации"),
        ("rejected", "Отклонено"),
    )

    title = models.CharField(
        max_length=100, verbose_name="Заголовок"
    )  # Заголовок записи
    content = models.TextField(verbose_name="Описание")  # Основное содержание записи
    slug = models.SlugField(
        **NULLABLE
    )  # Уникальный slug для записи (автоматически создается на основе заголовка)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        null=True,
    )  # Автор записи, связь с моделью пользователя
    is_published = models.BooleanField(
        default=False, verbose_name="Опубликовано"
    )  # Флаг публикации записи
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="no_published",
        verbose_name="Статус",
    )  # Статус записи
    preview = models.ImageField(
        upload_to="media/diary/images", verbose_name="Изображение", **NULLABLE
    )  # Изображение для предварительного просмотра записи
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания"
    )  # Дата создания записи
    views = models.IntegerField(
        default=0, verbose_name="Просмотры"
    )  # Количество просмотров записи

    def __str__(self):
        return f"{self.title} ({self.created_at}) - {self.views} просмотров"

    def get_unique_slug(self):
        """
        Генерация уникального slug для записи на основе её заголовка.

        Если slug для записи не задан, создается уникальный slug на основе транслитерации заголовка.
        Если уже существует запись с таким slug, добавляется номер для уникальности.
        """
        slug = slugify(self.title)  # Создаем slug с помощью транслитерации заголовка
        unique_slug = slug
        num = 1

        # Проверка на существование записи с таким же slug
        while Diary.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1

        return unique_slug

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматической генерации slug.

        Если slug не был установлен вручную, он генерируется автоматически на основе заголовка.
        """
        if not self.slug:
            self.slug = (
                self.get_unique_slug()
            )  # Автоматически генерируем уникальный slug
        super().save(*args, **kwargs)  # Сохраняем объект

    class Meta:
        verbose_name = "Запись в дневнике"
        verbose_name_plural = "Записи в дневнике"
        ordering = [
            "-created_at"
        ]  # Сортировка записей по дате создания (сначала новые)
        permissions = [
            ("can_moderate", "Может модерировать записи"),  # Право модерации записей
        ]


class Message(models.Model):
    """
    Модель для хранения сообщений между пользователями.

    Модель представляет собой систему сообщений между пользователями приложения.
    Каждое сообщение включает тему, текст сообщения, отправителя, получателя,
    а также статус прочтения и дату отправки.

    Поля модели:
        - subject: Тема сообщения.
        - body: Основное содержание сообщения.
        - sender: Отправитель сообщения (пользователь).
        - recipient: Получатель сообщения (пользователь).
        - is_read: Флаг прочтения сообщения.
        - created: Дата и время отправки сообщения.
    """

    subject = models.CharField(
        max_length=200, verbose_name="Тема сообщения", **NULLABLE
    )  # Тема сообщения (опционально)
    body = models.TextField(verbose_name="Сообщение")  # Основное содержание сообщения
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="sent_messages",
        **NULLABLE,
    )  # Отправитель сообщения (опционально)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="received_messages",
        **NULLABLE,
    )  # Получатель сообщения (опционально)
    is_read = models.BooleanField(
        default=False, verbose_name="Прочитано", null=True
    )  # Флаг прочтения сообщения
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата отправки"
    )  # Дата и время отправки сообщения

    def __str__(self):
        return f"Сообщение: {self.subject} от {self.sender}"

    class Meta:
        ordering = [
            "is_read",
            "-created",
        ]  # Сортировка сообщений (сначала непрочитанные, потом по дате создания)
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
