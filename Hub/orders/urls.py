from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderCreateAPIView.as_view(), name='order_create'),
    path('list/', views.OrderListAPIView.as_view(), name='order_list'),
    path('<uuid:id>/', views.OrderRetrieveAPIView.as_view(), name='order_detail'),
    path('o/<uuid:id>/', views.OrderRetrieveUpdateDestroyAPIView.as_view(), name='order_admin'),
]