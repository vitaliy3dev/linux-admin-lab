from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('api/status/', views.server_status, name='server_status'),
]
