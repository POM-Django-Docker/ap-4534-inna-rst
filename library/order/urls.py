from django.urls import path
from .views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView

app_name = 'order'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('edit/<int:pk>/', OrderUpdateView.as_view(), name='order_edit'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
]
