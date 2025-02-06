from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    # path('quiz-public/', views.quiz_public_view, name='quiz_public'),
    # path('quiz-self/', views.quiz_self_view, name='quiz_self'),
    path('quiz-result/', views.quiz_result_view, name='quiz_result'),
    ]