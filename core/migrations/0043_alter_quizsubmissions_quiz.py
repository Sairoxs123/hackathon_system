# Generated by Django 4.1.7 on 2024-11-12 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0042_quizsubmissions_quiz"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizsubmissions",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.quiz"
            ),
        ),
    ]