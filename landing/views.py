from django.shortcuts import render

# Create your views here.
def landing_view(request):
    return render(request, 'landing.html')

def quiz_result_view(request):
    return render(request, 'quiz_result.html')