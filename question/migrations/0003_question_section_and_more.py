# Generated by Django 4.1.7 on 2023-04-18 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0002_alter_section_minimum_score'),
        ('question', '0002_alter_question_scores'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='section.section'),
            preserve_default=False,
        ),
        migrations.AlterOrderWithRespectTo(
            name='question',
            order_with_respect_to='section',
        ),
    ]
