# Generated by Django 4.1.7 on 2025-01-11 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0049_users_competition_points_users_question_points_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="users",
            name="points",
        ),
    ]
