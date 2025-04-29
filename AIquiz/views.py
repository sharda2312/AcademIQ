from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from quiz.models import Quiz, Question, UserAnswer, QuizResult
from django.contrib.auth.decorators import login_required
import os
import json
from groq import Groq
import re
from django.views.decorators.http import require_http_methods

def generate_quiz_questions(context):
    """Utility function to generate quiz questions from the AI API"""
    try:
        question_count = context.get('question_count')
        grade = context.get('grade')
        topics = context.get('topics')
        model = context.get('model')
        level = context.get('level')
        
        # Check if all required fields are present
        if not all([question_count, grade, topics, model, level]):
            return {"success": False, "error": "Missing required parameters"}, 400
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"success": False, "error": "API key not configured"}, 500
            
        client = Groq(api_key=api_key)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""Generate {question_count} {level} level multiple-choice questions for {grade} grade students on the topic of {topics}. 
                    Ensure the questions vary in type, including definitions, applications, and analyses, 
                    and span a range of difficulty levels from easy to challenging, student is indian. 
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
            model=f"{model}",
        )

        # Get AI-generated response
        ai_response = chat_completion.choices[0].message.content
        
        # Extract the JSON part using regex
        match = re.search(r"\[\s*{.*}\s*\]", ai_response, re.DOTALL)
        if match:
            json_string = match.group(0)  # Extract JSON content
            questions_data = json.loads(json_string)  # Convert to Python list
            return {"success": True, "data": questions_data}, 200
        else:
            return {"success": False, "error": "Could not extract JSON from AI response. Check your topics for the quiz are  appropriate, else retry"}, 500
            
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON received from AI: {str(e)}"}, 500
    except Exception as e:
        return {"success": False, "error": f"Error generating quiz: {str(e)}"}, 500

@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def AI_create_quiz(request):
    """View for creating an AI-generated quiz (web interface)"""
    if request.method == "POST":
        # Extract form data
        question_count = request.POST.get('questions_count')
        level = request.POST.get('level')
        grade = request.POST.get('grade')
        topics = request.POST.get('topics')
        model = request.POST.get('model')
        
        # Validate required fields
        if not all([question_count, level, grade, topics, model]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": "All fields are required"}, status=400)
            else:
                # For form submissions, redirect back with error message
                # You might want to add Django messages framework here
                return render(request, 'AI_create_quiz.html', {"error": "All fields are required"})
        
        context = {
            "question_count": question_count,
            "grade": grade,
            "topics": topics,
            "model": model,
            "level": level,
        }
        
        request.session['quiz_context'] = context
        
        return redirect('ai')
    
    return render(request, 'AI_create_quiz.html')

@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def self_AI_create_quiz(request):
    """View for creating a self-attempt AI-generated quiz (web interface)"""
    if request.method == "POST":
        # Extract form data
        question_count = request.POST.get('questions_count')
        level = request.POST.get('level')
        grade = request.POST.get('grade')
        topics = request.POST.get('topics')
        model = request.POST.get('model')
        
        # Validate required fields
        if not all([question_count, level, grade, topics, model]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": "All fields are required"}, status=400)
            else:
                return render(request, 'AI_create_quiz.html', {"error": "All fields are required"})
        
        context = {
            "question_count": question_count,
            "grade": grade,
            "topics": topics,
            "model": model,
            "level": level,
        }
        
        request.session['quiz_context'] = context
        
        return redirect('self-attempt-quiz')
    
    return render(request, 'AI_create_quiz.html')

@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def ai(request):
    """View for displaying and saving AI-generated quiz (web interface)"""
    # Check if quiz context exists in session
    if 'quiz_context' not in request.session:
        return HttpResponse("No quiz context found", status=400)
    
    # Generate quiz questions
    response, status_code = generate_quiz_questions(request.session.get('quiz_context'))
    
    if not response['success']:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(response, status=status_code)
        else:
            return HttpResponse(response['error'], status=status_code)
    
    questions_data = response['data']
    
    if request.method == "POST":
        quiz_title = request.POST.get("title")
        time_limit = request.POST.get("time_limit")
        marking_scheme = request.POST.get("marking_scheme")
        
        # Validate required fields
        if not all([quiz_title, time_limit, marking_scheme]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": "All fields are required"}, status=400)
            else:
                return render(request, 'ai.html', {"questions": questions_data, "error": "All fields are required"})
        
        user = request.user
        context = request.session.get('quiz_context')
        question_count = context.get('question_count')
        
        try:
            # Create the quiz
            quiz = Quiz.objects.create(
                user=user,
                title=quiz_title,
                time_limit=time_limit,
                marking_scheme=marking_scheme,
                question_count=question_count
            )

            # Loop through questions
            question_texts = request.POST.getlist("question_text[]")  
            options1 = request.POST.getlist("option1[]")
            options2 = request.POST.getlist("option2[]")
            options3 = request.POST.getlist("option3[]")
            options4 = request.POST.getlist("option4[]")
            correct_options = request.POST.getlist("correct_option[]")

            # Validate input data lengths match
            if not (len(question_texts) == len(options1) == len(options2) == len(options3) == len(options4) == len(correct_options)):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({"success": False, "error": "Question data is incomplete"}, status=400)
                else:
                    return render(request, 'ai.html', {"questions": questions_data, "error": "Question data is incomplete"})

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

            # Clear session data after successful save
            if 'quiz_context' in request.session:
                del request.session['quiz_context']
                request.session.modified = True

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "quiz_code": quiz.quiz_code})
            else:
                return render(request, "create_quiz_success.html", {"quiz_code": quiz.quiz_code})
                
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": str(e)}, status=500)
            else:
                return render(request, 'ai.html', {"questions": questions_data, "error": str(e)})

    # GET request - display the form with AI-generated questions
    return render(request, 'ai.html', {"questions": questions_data})

# API endpoint for generating quiz questions
@csrf_protect
@login_required
@require_http_methods(["POST"])
def api_generate_quiz(request):
    """API endpoint for generating quiz questions"""
    try:
        data = json.loads(request.body)
        
        # Extract request data
        question_count = data.get('question_count')
        grade = data.get('grade')
        topics = data.get('topics')
        model = data.get('model', 'deepseek-r1-distill-llama-70b')  # Default model
        level = data.get('level', 'moderate')  # Default level
        
        # Validate required fields
        if not all([question_count, grade, topics]):
            return JsonResponse({"success": False, "error": "Missing required parameters"}, status=400)
        
        context = {
            "question_count": question_count,
            "grade": grade,
            "topics": topics,
            "model": model,
            "level": level,
        }
        
        # Generate quiz questions
        response, status_code = generate_quiz_questions(context)
        return JsonResponse(response, status=status_code)
        
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON in request body"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@login_required
def self_quiz_home(request):
    """View for self-quiz home page (web interface)"""
    return render(request, "self_quiz_home.html")

@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def self_attempt_quiz(request):
    """View for attempting an AI-generated quiz (web interface)"""
    if request.method == "GET":
        # Check if quiz context exists in session
        if 'quiz_context' not in request.session:
            return HttpResponse("No quiz context found", status=400)
            
        # Check if questions are already in session
        questions_data = request.session.get('quiz_questions')
        
        if not questions_data:
            # Generate new questions
            response, status_code = generate_quiz_questions(request.session.get('quiz_context'))
            
            if not response['success']:
                return HttpResponse(response['error'], status=status_code)
                
            questions_data = response['data']
            
            # Store questions in session
            request.session['quiz_questions'] = questions_data
            request.session.modified = True

        return render(request, 'self_attempt_quiz.html', {
            "questions": questions_data,
            "question_count": len(questions_data)
        })

    elif request.method == "POST":
        user = request.user
        context = request.session.get('quiz_context', {})
        question_count = int(context.get('question_count', 0))

        # Retrieve stored quiz questions
        questions_data = request.session.get('quiz_questions')
        
        if not questions_data:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": "Quiz questions not found"}, status=400)
            else:
                return HttpResponse("Quiz questions not found", status=400)

        try:
            # Create a new quiz instance
            quiz = Quiz.objects.create(
                user=user, 
                question_count=question_count,
                title=f"Self-attempt Quiz on {context.get('topics', 'Various Topics')}"
            )

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
            result = QuizResult.objects.create(
                user=user,
                quiz=quiz,
                total_marks=total_marks,
                obtained_marks=obtained_marks
            )

            # Clear session data after successful submission
            if 'quiz_questions' in request.session:
                del request.session['quiz_questions']
                request.session.modified = True
                
            if 'quiz_context' in request.session:
                del request.session['quiz_context']
                request.session.modified = True

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    "success": True, 
                    "quiz_code": quiz.quiz_code,
                    "total_marks": total_marks,
                    "obtained_marks": obtained_marks
                })
            else:
                return redirect('result', quiz_code=quiz.quiz_code)
                
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "error": str(e)}, status=500)
            else:
                return HttpResponse(f"Error processing quiz: {str(e)}", status=500)