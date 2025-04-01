from django.urls import path
from . import views

urlpatterns = [
    path('result/<str:quiz_code>/result/', views.result_view, name='result'),
]