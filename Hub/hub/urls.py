from django.urls import path
from . import views


urlpatterns = [
    path('', views.ClientListCreateAPIView.as_view()),
    path('client/<slug:slug>/', views.ClientRetrieveUpdateDestroy.as_view(), name='cd_detail_slug'),
    path('client/<int:id>/', views.ClientRetrieveUpdateDestroy.as_view(), name='cd_detail_id')
]