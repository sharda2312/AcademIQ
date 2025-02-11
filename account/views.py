from django.shortcuts import render, HttpResponse
from authapp.models import User
from quiz.models import QuizResult

# Create your views here.h


def account(request):
    user = request.user
    user1 = User.objects.filter(email = user)[0]
    quizs = QuizResult.objects.filter(user=user).order_by('-submitted_at')
    for q in quizs:
        print(q.quiz.title)
    
    context = {
        "quizs" : quizs,
        "user" : user1,
    }
       
    return render(request, "account.html", context)