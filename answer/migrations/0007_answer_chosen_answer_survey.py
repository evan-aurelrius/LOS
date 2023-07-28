# Generated by Django 4.1.7 on 2023-04-21 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0001_initial"),
        ("answer", "0006_alter_answer_unique_together_remove_answer_chosen_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="chosen",
            field=models.CharField(default="DefAns", max_length=200),
            preserve_default=False,
        ),
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