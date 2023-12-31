# Generated by Django 4.1.7 on 2023-04-21 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("application", "0005_collateral_application"),
        ("section", "0002_alter_section_minimum_score"),
        ("survey", "0003_alter_survey_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(name="survey", unique_together=set(),),
        migrations.AddField(
            model_name="survey",
            name="application",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="application.application",
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="survey", unique_together={("filler", "application", "section")},
        ),
        migrations.RemoveField(model_name="survey", name="applicant",),
    ]
