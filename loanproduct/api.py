from datetime import datetime, timedelta
from typing import List

from django.db.models import Q, CharField, Count
from django.db.models.functions import Cast, TruncMinute
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja.errors import HttpError
from ninja.pagination import paginate
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from loanproduct.models import LoanProduct, LoanProductSection
from loanproduct.schemas import LoanProductSchema, LoanProductPayloadSchema, LoanProductResponseSchema, SectionSchema, \
    ErrorMessage
from loanproduct.service import get_filtered_objects
from section.models import Section


@api_controller('/loanproduct', tags=['Loan Product'])
class LoanProductController:

    @route.post('', response={200: LoanProductResponseSchema}, auth=JWTAuth())
    def create_loan_product(self, payload: LoanProductPayloadSchema):
        product = LoanProduct.objects.create(**payload.dict())
        return 200, {"message": f"{product.name} successfully created", "loan_product_id": product.id}

    @route.get('/list', response=List[LoanProductSchema], auth=JWTAuth())
    @paginate()
    def get_loan_product_list(
            self,
            product_id: str = None,
            product_name: str = None,
            description: str = None,
            category: str = None,
            create_date_start: str = None,
            create_date_end: str = None,
            update_date_start: str = None,
            update_date_end: str = None
    ):
        query = Q()
        dateformat = '%Y-%m-%d'
        loanproducts = get_filtered_objects(LoanProduct, query, dateformat, id=product_id, name=product_name,
                                            description=description, category=category,
                                            create_date_start=create_date_start,
                                            create_date_end=create_date_end, update_date_start=update_date_start,
                                            update_date_end=update_date_end)
        return list(loanproducts)

    @route.get('/{product_id}', response={200: LoanProductSchema}, auth=JWTAuth())
    def get_loan_product_detail(self, product_id: int):
        try:
            product = LoanProduct.objects.annotate(
                created_date=Cast(TruncMinute("create_date"), CharField()),
                updated_date=Cast(TruncMinute("update_date"), CharField())
            ).get(id=product_id)
            return 200, product
        except LoanProduct.DoesNotExist:
            raise HttpError(404, "Loan product does not exist")

    @route.put('/{product_id}', response={200: LoanProductResponseSchema}, auth=JWTAuth())
    def update_loan_product(self, product_id: int, payload: LoanProductPayloadSchema):
        product = get_object_or_404(LoanProduct, id=product_id)
        for attr, value in payload.dict().items():
            setattr(product, attr, value)
        product.update_date = timezone.localtime(timezone.now())
        product.save()
        return 200, {"message": f"{product.name} successfully updated", "loan_product_id": product.id}

    @route.delete('/{product_id}', response={200: LoanProductResponseSchema}, auth=JWTAuth())
    def delete_loan_product(self, request, product_id: int):
        product = get_object_or_404(LoanProduct, id=product_id)
        product_name = product.name
        product_id = product.id
        product.delete(user=request.user)
        return 200, {"message": f"{product_name} successfully deleted", "loan_product_id": product_id}

    @route.get('sections/{product_id}', response={200: List[SectionSchema]}, auth=JWTAuth())
    def get_loan_product_section(self, product_id: int):
        product = get_object_or_404(LoanProduct, id=product_id)
        sections = product.sections.order_by('loanproductsection').annotate(
            created_date=Cast(TruncMinute("create_date"), CharField()),
            updated_date=Cast(TruncMinute("update_date"), CharField()),
            question_count=Count('question')
        )
        return 200, list(sections)

    @route.post('sections/{product_id}', response={200: LoanProductResponseSchema, 400: ErrorMessage}, auth=JWTAuth())
    def update_loan_product_section(self, product_id: int, sections_id: List[int]):
        product = get_object_or_404(LoanProduct, id=product_id)
        matching_section_count = Section.objects.filter(id__in=sections_id).count()
        if len(sections_id) != matching_section_count:
            return 400, {"message": "Section doesnt match"}
        product.sections.clear()
        for i in range(len(sections_id)):
            section = get_object_or_404(Section, id=sections_id[i])
            LoanProductSection.objects.create(
                loan_product=product,
                section=section,
                order=i,
            )
        return 200, {"message": f"{product.name} section successfully updated", "loan_product_id": product.id}
