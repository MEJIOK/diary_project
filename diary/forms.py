from django import forms
from pytils.translit import slugify

from diary.models import Diary


class DiaryForm(forms.ModelForm):
    """
    Форма для создания новой записи в дневнике.

    Эта форма используется для сбора данных от пользователя при создании новой записи.
    Она отображает поля для заголовка, содержания и загрузки изображения.
    Кроме того, в методе save происходит автоматическое создание slug (человеко-понятного URL),
    если оно не задано.

    Поля формы:
        - title: Заголовок записи (обязательное поле).
        - content: Основное содержание записи (обязательное поле).
        - preview: Изображение для предварительного просмотра записи (опционально).

    Виджеты:
        - Настраиваемые классы для улучшения внешнего вида полей формы (Bootstrap).
    """

    class Meta:
        model = Diary
        fields = ["title", "content", "preview"]  # Поля, отображаемые в форме
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),  # Стиль поля заголовка
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 6}
            ),  # Стиль текстового поля для содержания
            "preview": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),  # Стиль поля для загрузки изображения
        }

    def save(self, commit=True):
        """
        Переопределение метода сохранения.

        В этом методе происходит автоматическая генерация slug на основе заголовка,
        если slug еще не установлен.

        Аргументы:
            commit (bool): Если True, объект сразу сохраняется в базе данных.

        Возвращает:
            diary (Diary): Объект дневника после сохранения.
        """
        diary = super().save(
            commit=False
        )  # Создаем объект Diary, но пока не сохраняем его
        if not diary.slug:
            diary.slug = slugify(diary.title)  # Генерация slug на основе заголовка
        if commit:
            diary.save()  # Сохраняем объект в базе данных
        return diary


class DiaryUpdateForm(forms.ModelForm):
    """
    Форма для обновления существующей записи в дневнике.

    Эта форма похожа на форму создания, но используется для редактирования существующей записи.
    Как и в случае с созданием, если slug отсутствует, он генерируется автоматически.

    Поля формы:
        - title: Заголовок записи (обязательное поле).
        - content: Основное содержание записи (обязательное поле).
        - preview: Изображение для предварительного просмотра записи (опционально).

    Виджеты:
        - Настраиваемые классы для улучшения внешнего вида полей формы (Bootstrap).
    """

    class Meta:
        model = Diary
        fields = ["title", "content", "preview"]  # Поля для редактирования записи
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите заголовок"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Введите содержание",
                }
            ),
            "preview": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),  # Стиль для поля загрузки изображения
        }

    def save(self, commit=True):
        """
        Переопределение метода сохранения.

        Автоматическая генерация slug при необходимости, как и в форме создания.
        Аргументы:
            commit (bool): Если True, объект сразу сохраняется в базе данных.

        Возвращает:
            diary (Diary): Объект дневника после сохранения.
        """
        diary = super().save(
            commit=False
        )  # Создаем объект Diary, но пока не сохраняем его
        if not diary.slug:
            diary.slug = slugify(diary.title)  # Генерация slug на основе заголовка
        if commit:
            diary.save()  # Сохраняем объект в базе данных
        return diary
