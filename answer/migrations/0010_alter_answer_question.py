# Generated by Django 4.1.7 on 2023-05-12 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("answer", "0009_answer_survey"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=models.CharField(max_length=200),
        ),
    ]
