from django.db import models
from applicant.models import Applicant

class Financial(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.applicant} - {self.title} - {self.amount}"