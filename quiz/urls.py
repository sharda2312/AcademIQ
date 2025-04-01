from . import views
from django.urls import path

urlpatterns = [
    path('join-quiz/', views.join_quiz_view, name='join_quiz'),
    path('quiz-public/', views.quiz_public_view, name='quiz-public'),
    path('quiz-self/', views.quiz_self_view, name='quiz-self'),
    path('manual-quiz/', views.create_manual_quiz, name='manual-quiz'),
    path('quiz/<str:quiz_code>/', views.quiz_view, name='quiz_view'),
    path('quiz/<str:quiz_code>/attempt/', views.attempt_quiz, name='attempt_quiz'),
    path('quiz/<str:quiz_code>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<str:quiz_code>/questions/', views.quiz_questions, name='questions'),

    # path('quiz', views.quiz, name='quiz'),
    # path()
]   