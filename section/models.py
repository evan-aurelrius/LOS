from django.db import models
from django.utils import timezone

from loanproduct.softdeletemodel import SoftDeleteModel


class Section(SoftDeleteModel):
    name = models.CharField(max_length=100)
    minimum_score = models.PositiveIntegerField(null=True, blank=True, default=0)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
