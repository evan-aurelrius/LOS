from django.contrib import admin

from loanproduct.softdeletemodel import SoftDeleteModelAdmin
from .models import Applicant, ApplicantFile

admin.site.register(Applicant)
admin.site.register(ApplicantFile, SoftDeleteModelAdmin)