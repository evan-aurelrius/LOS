# Generated by Django 4.1.7 on 2023-05-12 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0004_alter_survey_unique_together_survey_application_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="survey", name="final_score",),
    ]
