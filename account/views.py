from django.shortcuts import render, HttpResponse
from authapp.models import User
from quiz.models import QuizResult

# Create your views here.h

def account(request):
    user = request.user
    user1 = User.objects.filter(email = user)[0]
    quiz = QuizResult.objects.filter(user=user)
    for q in quiz:
        print(user1.name)
    
    context = {
        "quiz" : quiz,
        "user" : user1,
    }
       
    return render(request, "account.html", context)