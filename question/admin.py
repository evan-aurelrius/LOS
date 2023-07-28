from django.contrib import admin

from loanproduct.softdeletemodel import SoftDeleteModelAdmin
from .models import Question

admin.site.register(Question, SoftDeleteModelAdmin)