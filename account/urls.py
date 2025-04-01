from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account, name = 'account'),
    path('all-attempted-quiz/', views.all_attempted_quiz, name='all_attempted_quiz'),
    path('all-created-quiz/', views.all_created_quiz, name='all_created_quiz'),
]