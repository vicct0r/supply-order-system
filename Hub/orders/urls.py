from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderCreateAPIView.as_view()),
    path('<uuid:id>/', views.OrderRetrieveAPIView.as_view(), name='order_detail'),
    path('o/<uuid:id>/', views.OrderRetrieveUpdateDestroyAPIView.as_view()),
]