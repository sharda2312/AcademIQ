from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate,login, logout
import json
from .models import User


@csrf_protect
def signup_view(request):
    return render(request, 'register.html')
@csrf_protect
def logout_view(request):
    if 'user_name' in request.session:
        logout(request)
    return redirect("landing")
@csrf_protect
def check_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            email = data.get("email")
            if User.objects.filter(email=email).exists():
                return JsonResponse({"status": "error", "message": "Email already registered"}, status=200)  # Use 200 for frontend handling
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=200)

@csrf_protect
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
            password = data.get("password")  # In production, hash the password
            dob = data.get("dob")
            
            
            # Hash the password before storing it
            password = make_password(password)

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({"status": "error", "message": "Email already registered."}, status=200)

            # Create the user
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,  # Hashing should be used in real apps
                dob=dob
            )

            return JsonResponse({"status": "success", "message": "User registered successfully"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # ✅ Authenticate using email (not username)
            user = authenticate(request, email=email, password=password)

            # Validate password
            if user is not None:  # Correct way to check password
                login(request, user)  # Storing session manually
                request.session['user_name'] = user.first_name
                return JsonResponse({"status": "success", "message": "Login successful", "redirect_url": "/"})
            else:
                return JsonResponse({"status": "error", "message": "Invalid email or password"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User does not exist"}, status=400)

    return render(request, 'login.html')
