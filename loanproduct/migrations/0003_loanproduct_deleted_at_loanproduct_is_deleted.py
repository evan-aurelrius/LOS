# Generated by Django 4.1.7 on 2023-05-07 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanproduct', '0002_alter_loanproduct_create_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanproduct',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
