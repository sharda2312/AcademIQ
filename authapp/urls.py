from django.urls import path
from .views import register_user, signup_view, check_email, login_view, logout_view



urlpatterns = [
    path("register/", register_user, name="register"),
    path("signup/", signup_view, name="signup"),
    path('check-email/', check_email, name='check-email'), 
    path('login/', login_view, name = "login"), 
    path('logout/', logout_view, name="logout"),
]