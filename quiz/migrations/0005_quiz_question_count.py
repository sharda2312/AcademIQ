# Generated by Django 5.1.4 on 2025-03-28 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0004_alter_quiz_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="question_count",
            field=models.PositiveIntegerField(default=5),
        ),
    ]
