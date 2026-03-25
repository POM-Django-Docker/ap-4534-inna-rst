from django.urls import path
from .views import BookListView, BookCreateView, BookUpdateView, BookDeleteView

app_name = 'book'

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('edit/<int:pk>/', BookUpdateView.as_view(), name='book_edit'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
]