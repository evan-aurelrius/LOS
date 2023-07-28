from django.db import models
from django.utils import timezone

from account.models import User
from loanproduct.softdeletemodel import SoftDeleteModel
from section.models import Section


class LoanProduct(SoftDeleteModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    sections = models.ManyToManyField(
        Section,
        through='LoanProductSection',
        through_fields=('loan_product', 'section'),
    )

    def __str__(self):
        return self.name


class LoanProductSection(models.Model):
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('loan_product', 'section')
        ordering = ('order',)

    def __str__(self):
        return f'{self.loan_product} - {self.section}'
