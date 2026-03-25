from django.urls import path
from .views import (
    AuthorCreateView, AuthorDeleteView,
    AuthorListView,   AuthorUpdateView,
)

app_name = 'author'
urlpatterns = [
    path("", AuthorListView.as_view(), name="author_list"),
    path("create/", AuthorCreateView.as_view(), name="author_create"),
    path("edit/<int:pk>/", AuthorUpdateView.as_view(), name="author_edit"),
    path("delete/<int:pk>/", AuthorDeleteView.as_view(), name="author_delete"),
]