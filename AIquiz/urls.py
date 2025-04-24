from django.urls import path
from . import views

urlpatterns = [
    # Web interfaces
    path('ai/', views.ai, name='ai'),
    path('ai-create-quiz/', views.AI_create_quiz, name='ai-create-quiz'),
    path('self-ai-create-quiz/', views.self_AI_create_quiz, name='self-ai-create-quiz'),
    path('self-quiz-home/', views.self_quiz_home, name='self-quiz-home'),
    path('self-attempt-quiz/', views.self_attempt_quiz, name='self-attempt-quiz'),
    
    # API endpoints
    path('api/generate-quiz/', views.api_generate_quiz, name='api-generate-quiz'),
]