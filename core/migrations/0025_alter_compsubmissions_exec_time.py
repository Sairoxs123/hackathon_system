# Generated by Django 4.1.7 on 2024-09-08 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0024_compsubmissions_memory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="compsubmissions",
            name="exec_time",
            field=models.FloatField(verbose_name="Execution Time"),
        ),
    ]
