from django.db import models
from application.models import Application
from section.models import Section
from account.models import User

class Survey(models.Model):
    filler = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    final_score = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        unique_together = ('application', 'section')

    def __str__(self):
        return f"{self.application.applicant.fullname} survey's from section {self.section.name}  with final score: {self.final_score}"