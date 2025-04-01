from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from authapp.models import User
from quiz.models import QuizResult, Quiz

# Create your views here.h

@login_required
def account(request):
    user = request.user
    user1 = User.objects.filter(email = user)[0]
    created_quiz = Quiz.objects.filter(user = user).order_by('-created_at')
    quizs = QuizResult.objects.filter(user=user).order_by('-submitted_at')
     
    context = {
        "quizs" : quizs,
        "user" : user1,
        "created_quiz": created_quiz,
    }
       
    return render(request, "account.html", context)

@login_required   
def all_attempted_quiz(request):
    user = request.user
    quiz = QuizResult.objects.filter(user=user).order_by('-submitted_at')
    return render(request, 'all_attempted_quiz.html', {"quiz": quiz})

@login_required
def all_created_quiz(request):
    user = request.user
    quiz = Quiz.objects.filter(user=user).order_by('-created_at')
    return render(request,'all_created_quiz.html', {"quiz":quiz})