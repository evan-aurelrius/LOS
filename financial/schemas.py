from ninja.orm import create_schema
from .models import Financial

FinancialSchema = create_schema(Financial, exclude=["applicant"])
