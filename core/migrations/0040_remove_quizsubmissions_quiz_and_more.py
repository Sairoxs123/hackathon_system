# Generated by Django 4.1.7 on 2024-11-12 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0039_alter_quiz_difficulty"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quizsubmissions",
            name="quiz",
        ),
        migrations.RemoveField(
            model_name="quizsubmissions",
            name="score",
        ),
        migrations.AddField(
            model_name="quizsubmissions",
            name="correct",
            field=models.BooleanField(default=False, verbose_name="Correct"),
        ),
        migrations.AddField(
            model_name="quizsubmissions",
            name="question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.question",
            ),
        ),
    ]