from django.contrib import admin

from loanproduct.models import LoanProduct
from loanproduct.softdeletemodel import SoftDeleteModelAdmin

admin.site.register(LoanProduct, SoftDeleteModelAdmin)
