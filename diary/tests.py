from django.core import mail
from django.test import TestCase
from django.urls import reverse

from diary.models import Diary
from users.models import User


class DiaryDetailViewTest(TestCase):
    """
    Тесты для представления детального просмотра записи в дневнике.

    Эти тесты проверяют такие аспекты, как:
    - Увеличение счетчика просмотров для опубликованных записей.
    - Доступ владельца к неопубликованным записям.
    - Ограничение доступа к неопубликованным записям для других пользователей.
    - Отправка email уведомления при достижении 100 просмотров.
    - Изменение статуса записи на "moderation" при отправке POST-запроса.
    """

    def setUp(self):
        """
        Настраиваем тестовые данные:
        - Создаем пользователя.
        - Создаем опубликованную запись с 99 просмотрами.
        - Создаем неопубликованную запись с 0 просмотрами.
        """
        self.user = User.objects.create(email="testuser@localhost", password="password")

        # Создаем опубликованную запись
        self.published_diary = Diary.objects.create(
            title="Test Published Diary",
            content="Content of the published diary",
            author=self.user,
            is_published=True,
            views=99,
        )

        # Создаем неопубликованную запись
        self.unpublished_diary = Diary.objects.create(
            title="Test Unpublished Diary",
            content="Content of the unpublished diary",
            author=self.user,
            is_published=False,
            views=0,
        )

    def test_published_diary_view_counter(self):
        """
        Проверяет, увеличивается ли счетчик просмотров для опубликованной записи.
        После запроса страница должна быть доступна (код 200), а просмотры увеличены до 100.
        """
        response = self.client.get(
            reverse("diary:detail", kwargs={"slug": self.published_diary.slug})
        )
        self.published_diary.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.published_diary.views, 100)

    def test_unpublished_diary_access_by_author(self):
        """
        Проверяет доступ владельца к неопубликованной записи.
        Страница должна быть доступна владельцу (код 200).
        """
        log = self.client.login(email="testuser@localhost", password="password")
        response = self.client.get(
            reverse("diary:detail", kwargs={"slug": self.unpublished_diary.slug})
        )
        print(f"Логин - {log}")  # Вывод для отладки
        self.assertEqual(response.status_code, 200)

    def test_unpublished_diary_access_by_another_user(self):
        """
        Проверяет ограничение доступа для другого пользователя к неопубликованной записи.
        Пользователь должен получить ответ с кодом 403 (Permission Denied).
        """
        User.objects.create(email="anotheruser@localhost", password="password")
        self.client.login(email="anotheruser@localhost", password="password")
        response = self.client.get(
            reverse("diary:detail", kwargs={"slug": self.unpublished_diary.slug})
        )
        self.assertEqual(response.status_code, 403)  # Permission Denied

    def test_send_email_on_100_views(self):
        """
        Проверяет, отправляется ли уведомление по email при достижении записи 100 просмотров.
        После запроса должно быть отправлено одно письмо.
        """
        self.client.get(
            reverse("diary:detail", kwargs={"slug": self.published_diary.slug})
        )
        self.assertEqual(len(mail.outbox), 1)  # Проверяем, что письмо отправлено
        self.assertIn("Уведомление", mail.outbox[0].subject)  # Проверяем тему письма
        self.assertIn(
            self.published_diary.author.email, mail.outbox[0].to
        )  # Проверяем адресата

    def test_post_request_changes_status_to_moderation(self):
        """
        Проверяет изменение статуса записи на "moderation" при отправке POST-запроса.
        После отправки формы статус записи должен измениться.
        """
        self.client.login(email="testuser@localhost", password="password")
        self.client.post(
            reverse("diary:detail", kwargs={"slug": self.published_diary.slug}),
            {"publish": True},
        )
        self.published_diary.refresh_from_db()
        self.assertEqual(self.published_diary.status, "moderation")
