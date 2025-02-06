from django.shortcuts import render

# Create your views here.
def landing_view(request):
    return render(request, 'landing.html')

# def quiz_public_view(request):
#     return render(request, 'quiz_public.html')

# def quiz_self_view(request):
#     return render(request, 'quiz_self.html')

def quiz_result_view(request):
    return render(request, 'quiz_result.html')