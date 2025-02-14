from django.urls import path
from . import views

urlpatterns = [
    path('ai/', views.ai, name = 'ai'),
]