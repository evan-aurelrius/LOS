# Generated by Django 4.1.7 on 2023-04-21 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("answer", "0007_answer_chosen_answer_survey"),
    ]

    operations = [
        migrations.RemoveField(model_name="answer", name="survey",),
    ]
