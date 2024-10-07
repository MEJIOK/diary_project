from django.urls import path

from diary.apps import DiaryConfig
from diary.views import (DiaryCreateView, DiaryDeleteView, DiaryDetailView,
                         DiaryListView, DiaryModerationActionView,
                         DiaryModerationListView, DiaryUpdateView,
                         HomeListView)

# Установка имени приложения, которое будет использоваться в пространстве имен URL.
app_name = DiaryConfig.name

# Список URL маршрутов для приложения дневника
urlpatterns = [
    # Главная страница с опубликованными записями
    path("", HomeListView.as_view(), name="home"),
    # Страница модерации записей (только для пользователей с правами модерации)
    path("moderation/", DiaryModerationListView.as_view(), name="moderation_list"),
    # Действия модератора над записями (например, одобрение или отклонение записи)
    path(
        "moderation/<slug:slug>/action/",
        DiaryModerationActionView.as_view(),
        name="moderation_action",
    ),
    # Страница со списком всех записей пользователя
    path("diary/", DiaryListView.as_view(), name="list"),
    # Страница создания новой записи
    path("create/", DiaryCreateView.as_view(), name="create"),
    # Страница детального просмотра записи по slug
    path("<slug:slug>/", DiaryDetailView.as_view(), name="detail"),
    # Страница редактирования записи по slug
    path("update/<slug:slug>/", DiaryUpdateView.as_view(), name="update"),
    # Страница удаления записи по slug
    path("delete/<slug:slug>/", DiaryDeleteView.as_view(), name="delete"),
]
