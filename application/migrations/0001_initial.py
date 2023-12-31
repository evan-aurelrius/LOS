# Generated by Django 4.1.7 on 2023-03-07 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('tenure', models.IntegerField()),
                ('interest_rate', models.IntegerField()),
                ('interest_type', models.CharField(choices=[('Flat', 'Flat'), ('Anuitas 78', 'Anuitas 78'), ('Anuitas', 'Anuitas'), ('Efektif', 'Efektif'), ('Sliding', 'Sliding')], max_length=30)),
                ('usage_type', models.CharField(choices=[('Modal Kerja', 'Modal Kerja'), ('Investasi', 'Investasi'), ('Konsumsi', 'Konsumsi')], max_length=30)),
            ],
        ),
    ]
