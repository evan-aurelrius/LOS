from django.contrib import admin

from loanproduct.softdeletemodel import SoftDeleteModelAdmin
from section.models import Section

admin.site.register(Section, SoftDeleteModelAdmin)
