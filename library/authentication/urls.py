from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from . import views


app_name = 'authentication'
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', views.user_list_view, name='user_list'),
    path('user/<int:user_id>/', views.user_detail_view, name='user_detail'),
]