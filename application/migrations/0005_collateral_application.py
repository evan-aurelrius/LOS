# Generated by Django 4.1.7 on 2023-04-14 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_alter_application_interest_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collateral',
            name='application',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='application.application'),
            preserve_default=False,
        ),
    ]
