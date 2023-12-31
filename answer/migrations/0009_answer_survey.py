# Generated by Django 4.1.7 on 2023-04-21 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0002_survey_filler"),
        ("answer", "0008_remove_answer_survey"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="survey",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="survey.survey",
            ),
            preserve_default=False,
        ),
    ]
