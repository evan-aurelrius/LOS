from typing import List

from ninja import Field, ModelSchema, Schema
from application.models import ApplicantCustomColumn, Application
from applicant.models import Applicant

class ApplicationLoanProductSchema(ModelSchema):
    class Config:
        model = Application
        model_fields = [
            'loan_product',
        ]

class CustomColumnSchema(ModelSchema):
    class Config:
        model = ApplicantCustomColumn
        model_fields = [
            'column_name',
            'column_value',
        ]

class ApplicationSchema(Schema):
    amount: int 
    tenure: int = 0
    interest_rate: int = 0
    interest_type: str = ""
    usage_type: str

class GetLoanProductSchema(Schema):
    id: int
    name: str
    description: str
    category: str

class CollateralSchema(Schema):
    collateral_type: str = ""
    collateral_value: int = 0

class ApplicantIn(ModelSchema):
    custom_columns: List[CustomColumnSchema] = []
    application: ApplicationSchema = "Null"
    collateral: CollateralSchema = "Null"
    class Config:
        model = Applicant
        model_exclude = [
            'id',
            'create_date',
            'update_date',
            'update_by'
        ]

class ApplicantCreate(Schema):
    applicant_id: int

class ApplicantPut(Schema):
    message: str
    applicant_id: int

class ApplicantOut(ModelSchema):
    custom_columns: List[CustomColumnSchema] = []
    application: ApplicationSchema = "Null"
    collateral: CollateralSchema = "Null"
    class Config:
        model = Applicant
        model_fields = '__all__'

class ErrorMessage(Schema):
    message: str