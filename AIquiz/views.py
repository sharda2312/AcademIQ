from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from quiz.models import Quiz, Question,UserAnswer,QuizResult
from django.contrib.auth.decorators import login_required
import os
import json
from groq import Groq
import re

def ai_quiz(request):
    # Retrieve context from session
    context = request.session.get('quiz_context')
    
    if not context:
        return HttpResponse("No quiz context found in session", status=400)
    
    question_count = context.get('question_count')
    grade = context.get('grade')
    topics = context.get('topics')
    model = context.get('model')
    level = context.get('level')
    
    client = Groq(
        api_key = os.getenv("GROQ_API_KEY"),
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Generate {question_count} {level} level multiple-choice questions for {grade} grade students on the topic of {topics}. 
                Ensure the questions vary in type, including definitions, applications, and analyses, 
                and span a range of difficulty levels from easy to challenging, and question should be in context of india. 
                in json in the correct key value pair write the postion of the correct ans like if the first ans is correct write 1.
                json format should be
                    "question": "What do plants use from the sun to make their own food?",
                    "options": [
                    "Water",
                    "Air",
                    "Sunlight",
                    "Soil"
                    ],
                    "correct": "3"
                """,
            }
        ],
        model= f"{model}",
    )

    # Get AI-generated response
    ai_response = chat_completion.choices[0].message.content
    return ai_response
    

# Create your views here.
@csrf_protect
@login_required
def AI_create_quiz(request):
    if request.method == "POST":
        question_count = request.POST.get('questions_count')
        level = request.POST.get('level')
        grade = request.POST.get('grade')
        topics = request.POST.get('topics')
        model = request.POST.get('model')
        
        context = {
            "question_count": question_count,
            "grade": grade,
            "topics" : topics,
            "model": model,
            "level": level,
        }
        
        request.session['quiz_context'] = context
        
        return redirect('self-attempt-quiz')
    
    return render(request, 'AI_create_quiz.html')
    
@csrf_protect
@login_required
def ai(request):
    
    ai_response = ai_quiz(request)
    
    context = request.session.get("quiz_context")
    question_count = context.get('question_count')
    
    if request.method == "POST":
            quiz_title = request.POST.get("title")
            time_limit = request.POST.get("time_limit")
            marking_scheme = request.POST.get("marking_scheme")
            
            user = request.user
            
            # Create the quiz
            quiz = Quiz.objects.create(
                user = user,
                title=quiz_title,
                time_limit=time_limit,
                marking_scheme=marking_scheme,
                question_count=question_count
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

    try:
        # Extract the JSON part using regex
        match = re.search(r"\[\s*{.*}\s*\]", ai_response, re.DOTALL)
        if match:
            print("stop")
            json_string = match.group(0)  # Extract JSON content
            questions_data = json.loads(json_string)  # Convert to Python list
            return render(request, 'ai.html', {"questions":questions_data})
        else:
            return HttpResponse("Could not extract JSON from AI response 32", status=500)

    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON received from AI", status=500)
    
    
@login_required
def self_quiz_home(request):
    return render(request, "self_quiz_home.html")


def self_attempt_quiz(request):
    """ Display AI-generated quiz and save user responses """
    
    if request.method == "GET":
        # Check if questions are already stored in session
        questions_data = request.session.get('quiz_questions')

        if not questions_data:
            ai_response = ai_quiz(request)  # Generate quiz once
            try:
                match = re.search(r"\[\s*{.*}\s*\]", ai_response, re.DOTALL)
                if not match:
                    return HttpResponse("Could not extract JSON from AI response", status=500)

                questions_data = json.loads(match.group(0))  # Parse JSON

                # Store questions in session to maintain consistency
                request.session['quiz_questions'] = questions_data
                request.session.modified = True  
            except json.JSONDecodeError:
                return HttpResponse("Invalid JSON received from AI", status=500)

        return render(request, 'self_attempt_quiz.html', {"questions": questions_data})

    elif request.method == "POST":
        user = request.user
        context = request.session.get('quiz_context', {})
        question_count = context.get('question_count', 0)

        # Retrieve stored quiz questions
        questions_data = request.session.get('quiz_questions')
        if not questions_data:
            return HttpResponse("Quiz questions not found in session", status=500)

        # Create a new quiz instance
        quiz = Quiz.objects.create(user=user, question_count=question_count)

        total_marks = len(questions_data)  
        obtained_marks = 0

        for i, q_data in enumerate(questions_data):
            question = Question.objects.create(
                quiz=quiz,
                question_text=q_data["question"],
                option1=q_data["options"][0],
                option2=q_data["options"][1],
                option3=q_data["options"][2],
                option4=q_data["options"][3],
                correct_option=int(q_data["correct"])
            )

            selected_option = request.POST.get(f'q{i+1}', None)
            selected_option = int(selected_option) if selected_option else 0
            is_correct = selected_option == question.correct_option  

            UserAnswer.objects.create(
                user=user,
                quiz=quiz,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

            if is_correct:
                obtained_marks += 1

        # Save quiz result
        QuizResult.objects.create(
            user=user,
            quiz=quiz,
            total_marks=total_marks,
            obtained_marks=obtained_marks
        )

        # Clear quiz session data to prevent reuse
        del request.session['quiz_questions']

        return render(request, "create_quiz_success.html", {"quiz_code": quiz.quiz_code})
