from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


# Create your views here.
@csrf_protect
def landing_view(request):
    return render(request, 'landing.html')

# @csrf_protect
# @login_required
# def quiz_result_view(request):
#     return render(request, 'quiz_result.html')