from typing import List

from ninja import ModelSchema, Schema

from loanproduct.models import LoanProduct


class LoanProductSchema(Schema):
    id: str
    name: str
    description: str
    category: str
    created_date: str
    updated_date: str


class SectionSchema(Schema):
    id: str
    name: str
    question_count: int
    minimum_score: int
    created_date: str
    updated_date: str


class LoanProductPayloadSchema(ModelSchema):
    class Config:
        model = LoanProduct
        model_exclude = [
            'id',
            'create_date',
            'update_date',
            'is_deleted',
            'deleted_at',
            'deleted_by',
            'sections',
        ]


class LoanProductResponseSchema(Schema):
    message: str
    loan_product_id: int


class ErrorMessage(Schema):
    message: str
