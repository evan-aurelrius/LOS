# Generated by Django 4.1.7 on 2023-03-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0007_alter_applicant_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='identity_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='identity_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='identity_district',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='identity_postal_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='identity_subdistrict',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('Kawin', 'Kawin'), ('Belum Kawin', 'Belum Kawin'), ('Cerai', 'Cerai')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='occupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='office_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='office_business_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='office_department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='office_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='office_phone_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='religion',
            field=models.CharField(blank=True, choices=[('Islam', 'Islam'), ('Kristen Protestan', 'Kristen Protestan'), ('Kristen Katolik', 'Kristen Katolik'), ('Hindu', 'Hindu'), ('Buddha', 'Buddha'), ('Konghucu', 'Konghucu'), ('Agama Lainnya', 'Agama Lainnya')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='surname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='tax_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
