from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from quiz.models import Quiz, QuizResult, UserAnswer



# Create your views here
@csrf_protect
@login_required
def result_view(request, quiz_code):
    quiz = get_object_or_404(Quiz, quiz_code=quiz_code)
    user = request.user
    result = get_object_or_404(QuizResult, user=user, quiz=quiz)

    answers = UserAnswer.objects.filter(user=user, quiz=quiz)

    return render(request, 'result.html', {
        'quiz': quiz,
        'result': result,
        'answers': answers,
    })
    