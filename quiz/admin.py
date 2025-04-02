from django.contrib import admin
from .models import Quiz, QuizResult, Question, UserAnswer

admin.site.register(Quiz)
admin.site.register(QuizResult)
admin.site.register(Question)
admin.site.register(UserAnswer)