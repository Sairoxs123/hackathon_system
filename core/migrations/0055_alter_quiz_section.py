# Generated by Django 4.1.7 on 2025-01-18 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0054_alter_updates_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="section",
            field=models.CharField(max_length=1, null=True, verbose_name="Section"),
        ),
    ]
