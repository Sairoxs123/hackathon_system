# Generated by Django 4.1.7 on 2024-11-11 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0038_quiz_difficulty"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="difficulty",
            field=models.CharField(
                default="Easy", max_length=10, verbose_name="Difficulty"
            ),
        ),
    ]
