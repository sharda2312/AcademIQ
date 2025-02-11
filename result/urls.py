from django.urls import path
from . import views

urlpatterns = [
    path('result/<str:quiz_code>/result/', views.result_view, name='result'),
    path('all-attempted-quiz/', views.all_attempted_quiz, name='all_attempted_quiz'),
]