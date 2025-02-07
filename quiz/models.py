from django.db import models
import random
import string
from authapp.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes", default=10)
    marking_scheme = models.CharField(
        max_length=10,
        choices=[
            ("1,0", "+1,0"), ("5,0", "+5,0"), ("4,0", "+4,0"),
            ("1,-0.25", "+1,-0.25"), ("1,-0.33", "+1,-0.33"),
            ("4,-1", "+4,-1"), ("4,-2", "+4,-2")
        ],
        default="1,0"
    )
    quiz_code = models.CharField(max_length=8, unique=True, blank=False, null=False)  # Ensure it's NOT blank or null

    def save(self, *args, **kwargs):
        if not self.quiz_code:  # Only generate if it doesn't exist
            self.quiz_code = self.generate_quiz_code()
        super().save(*args, **kwargs)

    def generate_quiz_code(self):
        """Generate a unique 8-character alphanumeric quiz code."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Quiz.objects.filter(quiz_code=code).exists():  # Ensure uniqueness
                return code

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    
    OPTION_CHOICES = [
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
    ]
    
    correct_option = models.PositiveSmallIntegerField(choices=OPTION_CHOICES)

    def __str__(self):
        return f"{self.quiz.title} - {self.question_text}"


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.IntegerField()
    is_correct = models.BooleanField()