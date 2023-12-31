# Generated by Django 4.1.7 on 2023-05-18 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "applicant",
            "0011_applicantfile_deleted_at_applicantfile_deleted_by_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Financial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("amount", models.IntegerField()),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="applicant.applicant",
                    ),
                ),
            ],
        ),
    ]
