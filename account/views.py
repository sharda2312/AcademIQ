from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from authapp.models import User
from quiz.models import QuizResult

# Create your views here.h

@login_required
def account(request):
    user = request.user
    user1 = User.objects.filter(email = user)[0]
    quizs = QuizResult.objects.filter(user=user).order_by('-submitted_at')
     
    context = {
        "quizs" : quizs,
        "user" : user1,
    }
       
    return render(request, "account.html", context)