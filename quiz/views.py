from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question
from django.http  import JsonResponse
from django.utils.timezone import now

# Create your views here.
@login_required
def join_quiz_view(request):
    if request.method == "POST":
        quiz_code = request.POST.get("quiz_code")

        # Check if quiz exists
        quiz = Quiz.objects.filter(quiz_code=quiz_code).first()
        if not quiz:
            return JsonResponse({"status": "error", "message": "Invalid quiz code."})

        # Redirect to quiz details page
        return redirect('quiz_view', quiz_code=quiz_code)

    return render(request, 'join_quiz.html')


@login_required
def quiz_view(request, quiz_code):
    quiz = get_object_or_404(Quiz, quiz_code=quiz_code)
    question_count = quiz.questions.count()
    positive_marks = int(quiz.marking_scheme.split(",")[0].strip("+"))
    total_marks = positive_marks * question_count

    return render(request, 'quiz.html', {
        'quiz': quiz,
        'question_count': question_count,
        'total_marks': total_marks
    })


@login_required
def attempt_quiz(request, quiz_code):
    quiz = get_object_or_404(Quiz, quiz_code=quiz_code)
    questions = quiz.questions.all()  # Fetch all questions related to this quiz
    question_count = quiz.questions.count()
    positive_marks = int(quiz.marking_scheme.split(",")[0].strip("+"))
    total_marks = positive_marks * question_count
    return render(request, 'attempt_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'time_limit': quiz.time_limit * 60,  # Convert minutes to seconds for the timer
        'question_count': question_count,
        'total_marks': total_marks,
    })


@login_required
def quiz_public_view(request):
    return render(request, 'quiz_public.html')

@login_required
def quiz_self_view(request):
    return render(request, 'quiz_self.html')

@login_required
def create_manual_quiz(request):
    if request.method == "POST":
        quiz_title = request.POST.get("title")
        time_limit = request.POST.get("time_limit")
        marking_scheme = request.POST.get("marking_scheme")

        # Create the quiz
        quiz = Quiz.objects.create(
            title=quiz_title,
            time_limit=time_limit,
            marking_scheme=marking_scheme
        )

        # Loop through questions (assuming frontend submits multiple questions)
        question_texts = request.POST.getlist("question_text[]")  
        options1 = request.POST.getlist("option1[]")
        options2 = request.POST.getlist("option2[]")
        options3 = request.POST.getlist("option3[]")
        options4 = request.POST.getlist("option4[]")
        correct_options = request.POST.getlist("correct_option[]")

        for i in range(len(question_texts)):
            Question.objects.create(
                quiz=quiz,
                question_text=question_texts[i],
                option1=options1[i],
                option2=options2[i],
                option3=options3[i],
                option4=options4[i],
                correct_option=int(correct_options[i])
            )

                # Redirect to a success page and pass the quiz code
        return render(request, "create_quiz_success.html", {"quiz_code": quiz.quiz_code})


    return render(request, "create_manual_quiz.html")
