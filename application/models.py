from django.db import models
from applicant.models import Applicant
from loanproduct.models import LoanProduct


class Application(models.Model):
    INTEREST_TYPE_CHOICES = [
        ('Flat', 'Flat'),
        ('Anuitas 78', 'Anuitas 78'),
        ('Anuitas', 'Anuitas'),
        ('Efektif', 'Efektif'),
        ('Sliding', 'Sliding')
    ]

    USAGE_TYPE_CHOICES = [
        ('Modal Kerja', 'Modal Kerja'),
        ('Investasi', 'Investasi'),
        ('Konsumsi', 'Konsumsi')
    ]

    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE, null=True, blank=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    amount = models.IntegerField()
    tenure = models.IntegerField(blank=True, null=True)
    interest_rate = models.IntegerField(blank=True, null=True)
    interest_type = models.CharField(
        max_length=30,
        choices=INTEREST_TYPE_CHOICES,
        blank=True, 
        null=True
    )
    usage_type = models.CharField(
        max_length=30,
        choices=USAGE_TYPE_CHOICES,
        blank=True, 
        null=True
    )

    def __str__(self):
        return str(self.amount)

class ApplicantCustomColumn(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=100)
    column_value = models.CharField(max_length=100)

    def __str__(self):
        return "{}: {}".format(self.column_name, self.column_value)

class Collateral(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    collateral_type = models.CharField(max_length=30)
    collateral_value = models.IntegerField()

    def __str__(self):
        return str(self.collateral_type)