from django.urls import path
from . import views

urlpatterns = [
    path('ai/', views.ai, name = 'ai'),
    path('ai-create-quiz/', views.AI_create_quiz, name = 'ai-create-quiz')
]