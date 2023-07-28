from django.db import models
from question.models import Question
from account.models import User
from applicant.models import Applicant
from survey.models import Survey

class Answer(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    chosen = models.CharField(max_length=200, blank=False, null=False)
    score = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.chosen
