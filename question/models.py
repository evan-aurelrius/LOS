from django.db import models
from django.contrib.postgres.fields import ArrayField

from loanproduct.softdeletemodel import SoftDeleteModel
from section.models import Section


class Question(SoftDeleteModel):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    choices = ArrayField(models.CharField(max_length=200))
    scores = ArrayField(models.IntegerField())

    class Meta:
        order_with_respect_to = 'section'

    def __str__(self):
        return self.question