# Generated by Django 4.1.7 on 2023-05-23 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applicant", "0012_applicant_branch"),
    ]

    operations = [
        migrations.AddField(
            model_name="applicantfile",
            name="detail",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
