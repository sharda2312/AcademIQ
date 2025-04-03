# Generated by Django 5.1.4 on 2025-04-03 12:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(default="self", max_length=50)),
                (
                    "time_limit",
                    models.PositiveIntegerField(
                        default=10, help_text="Time limit in minutes"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("question_count", models.PositiveIntegerField(default=5)),
                (
                    "marking_scheme",
                    models.CharField(
                        choices=[
                            ("1,0", "+1,0"),
                            ("5,0", "+5,0"),
                            ("4,0", "+4,0"),
                            ("1,-0.25", "+1,-0.25"),
                            ("1,-0.33", "+1,-0.33"),
                            ("4,-1", "+4,-1"),
                            ("4,-2", "+4,-2"),
                        ],
                        default="1,0",
                        max_length=10,
                    ),
                ),
                ("quiz_code", models.CharField(max_length=8, unique=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_text", models.TextField()),
                ("option1", models.CharField(max_length=255)),
                ("option2", models.CharField(max_length=255)),
                ("option3", models.CharField(max_length=255)),
                ("option4", models.CharField(max_length=255)),
                (
                    "correct_option",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Option 1"),
                            (2, "Option 2"),
                            (3, "Option 3"),
                            (4, "Option 4"),
                        ]
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="quiz.quiz",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuizResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total_marks", models.IntegerField()),
                ("obtained_marks", models.IntegerField()),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quiz.quiz"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("selected_option", models.IntegerField()),
                ("is_correct", models.BooleanField()),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quiz.question"
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quiz.quiz"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
