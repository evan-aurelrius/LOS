# Generated by Django 4.1.7 on 2023-03-17 11:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("applicant", "0006_alter_applicant_application_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applicant",
            name="create_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]