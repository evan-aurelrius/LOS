import os

from django.db import models
from django.utils import timezone

from account.models import User
from loanproduct.softdeletemodel import SoftDeleteModel


class Applicant(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]

    GENDER_CHOICES = (
        ("Laki-laki", "Laki-laki"),
        ("Perempuan", "Perempuan"),
    )

    RELIGION_CHOICES = [
        ('Islam', 'Islam'),
        ('Kristen Protestan', 'Kristen Protestan'),
        ('Kristen Katolik', 'Kristen Katolik'),
        ('Hindu', 'Hindu'),
        ('Buddha', 'Buddha'),
        ('Konghucu', 'Konghucu'),
        ('Agama Lainnya', 'Agama Lainnya')
    ]

    MARITAL_STATUS_CHOICES = [
        ('Kawin', 'Kawin'),
        ('Belum Kawin', 'Belum Kawin'),
        ('Cerai', 'Cerai')
    ]

    fullname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateField(default=timezone.now)
    update_date = models.DateTimeField(blank=True, null=True)
    update_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    application_status = models.CharField(
        max_length=30,
        choices=APPLICATION_STATUS_CHOICES,
        default="Pending"
    )
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES
    )
    birth_place = models.CharField(max_length=100)
    birth_date = models.DateField()
    mother_maiden_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    identity_number = models.CharField(max_length=100)
    tax_number = models.CharField(max_length=100, blank=True, null=True)
    religion = models.CharField(
        max_length=30,
        choices=RELIGION_CHOICES,
        blank=True,
        null=True
    )
    marital_status = models.CharField(
        max_length=30,
        choices=MARITAL_STATUS_CHOICES,
        blank=True,
        null=True
    )
    dependants_count = models.IntegerField(blank=True, null=True)
    domicile_address = models.TextField()
    domicile_subdistrict = models.CharField(max_length=100)
    domicile_district = models.CharField(max_length=100)
    domicile_city = models.CharField(max_length=100)
    domicile_postal_code = models.CharField(max_length=100)
    identity_address = models.TextField(blank=True, null=True)
    identity_subdistrict = models.CharField(max_length=100, blank=True, null=True)
    identity_district = models.CharField(max_length=100, blank=True, null=True)
    identity_city = models.CharField(max_length=100, blank=True, null=True)
    identity_postal_code = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    office_name = models.CharField(max_length=100, blank=True, null=True)
    office_address = models.TextField(blank=True, null=True)
    office_business_type = models.CharField(max_length=100, blank=True, null=True)
    office_department = models.CharField(max_length=100, blank=True, null=True)
    office_phone_number = models.CharField(max_length=100, blank=True, null=True)
    annual_income = models.IntegerField(blank=True, null=True)
    branch = models.CharField(max_length=100, default='Pusat')

    def __str__(self):
        return self.fullname


def generate_path(self, filename):
    url = f"applicant_files/{self.applicant.id}/{filename}"
    return url


class ApplicantFile(SoftDeleteModel):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    file = models.FileField(upload_to=generate_path)
    detail = models.CharField(max_length=100)
    
    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def extension(self):
        return os.path.splitext(self.file.name)[1]
