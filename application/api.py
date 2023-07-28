from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from applicant.models import Applicant
from application.models import Application
from application.schemas import CustomColumnSchema, ApplicantIn, ApplicantOut, ApplicantCreate, ApplicantPut, \
    ErrorMessage, ApplicationLoanProductSchema, GetLoanProductSchema
from application.services import ApplicantDetailService, ApplicationService, CollateralService, \
    ApplicantCustomColumnService
from django.forms.models import model_to_dict
from loanproduct.models import LoanProduct
from survey.models import Survey


@api_controller('/applicant', tags=['ApplicantDetail'])
class ApplicantDetailController:
    FORBIDDEN_COLUMNS_TO_CHANGE_ON_UPDATE = ["fullname", "gender", "birth_place", "birth_date", "mother_maiden_name",
                                             "phone_number", "email", "identity_number", "domicile_address",
                                             "domicile_subdistrict", "domicile_district", "domicile_city",
                                             "domicile_postal_code"]

    @route.post('', response={200: ApplicantCreate, 409: ErrorMessage})
    def create_applicant(self, request, payload: ApplicantIn):
        try:
            applicant = Applicant.objects.get(identity_number=payload.identity_number)
        except Applicant.DoesNotExist:
            applicant = None
        if applicant != None:
            return 409, {"message": "Applicant already exists"}
        payload_dict = payload.dict()
        payload_dict.pop("custom_columns")
        applicant_payload = payload_dict.copy()
        applicant_payload.pop("application")
        applicant_payload.pop("collateral")
        applicant = ApplicantDetailService.create_applicant(applicant_payload)
        application_payload = payload_dict["application"]
        if application_payload != "Null":
            application = ApplicationService.create_application(applicant, **application_payload)
            collateral_payload = payload_dict["collateral"]
            if collateral_payload != "Null":
                CollateralService.create_collateral(application, **collateral_payload)
        return 200, {"applicant_id": applicant.id}

    @route.get('/{applicant_id}', response={200: ApplicantOut, 404: ErrorMessage}, auth=JWTAuth())
    def get_applicant_detail(self, applicant_id: int):
        try:
            applicant = Applicant.objects.get(id=applicant_id)
            applicant_dict = model_to_dict(applicant)
            applicant_custom_columns = ApplicantCustomColumnService.get_all_applicant_custom_column(applicant)
            application = ApplicationService.get_application(applicant)
            collateral = None
            if application != None:
                collateral = CollateralService.get_collateral(application)
            applicant_dict["custom_columns"] = []
            for applicant_custom_column in applicant_custom_columns:
                applicant_dict["custom_columns"].append(
                    {
                        "column_name": applicant_custom_column.column_name,
                        "column_value": applicant_custom_column.column_value
                    }
                )
            if application != None:
                applicant_dict["application"] = {
                    "amount": application.amount,
                    "tenure": application.tenure,
                    "interest_rate": application.interest_rate,
                    "interest_type": application.interest_type,
                    "usage_type": application.usage_type
                }
                if collateral != None:
                    applicant_dict["collateral"] = {
                        "collateral_type": collateral.collateral_type,
                        "collateral_value": collateral.collateral_value
                    }
            return 200, applicant_dict
        except Applicant.DoesNotExist:
            return 404, {"message": "Applicant does not exist"}

    @route.put('/{applicant_id}', response={200: ApplicantPut, 404: ErrorMessage, 403: ErrorMessage}, auth=JWTAuth())
    def update_applicant_detail(self, request, applicant_id: int, payload: ApplicantIn):
        try:
            applicant = Applicant.objects.get(id=applicant_id)
            for column in self.FORBIDDEN_COLUMNS_TO_CHANGE_ON_UPDATE:
                if payload.dict()[column] != getattr(applicant, column):
                    return 403, {"message": "Forbidden to update applicant basic data"}
            payload_dict = payload.dict()
            applicant_payload = payload_dict.copy()
            applicant_payload.pop("custom_columns")
            applicant_payload.pop("application")
            ApplicantDetailService.update_applicant(applicant, applicant_payload)
            ApplicantCustomColumnService.update_or_create_applicant_custom_columns(applicant, payload_dict["custom_columns"])
            ApplicantCustomColumnService.delete_applicant_custom_columns_not_in_update(applicant, payload_dict["custom_columns"])
            application = ApplicationService.update_or_create_application(applicant, payload_dict["application"])
            CollateralService.update_or_create_collateral(application, payload_dict["collateral"])
            applicant.update_date = timezone.now()
            applicant.update_by = request.user
            applicant.save()
            return 200, {
                "message": "Applicant successfully updated",
                "applicant_id": applicant.id
            }
        except Applicant.DoesNotExist:
            return 404, {"message": "Applicant does not exist"}
        
    @route.post('/loan-product/{application_id}', response={200: ApplicationLoanProductSchema, 404: ErrorMessage}, auth=JWTAuth())
    def set_loan_product(self, application_id:int, payload: ApplicationLoanProductSchema):
        application = get_object_or_404(Application, id=application_id)
        loan_product = LoanProduct.objects.get(id=payload.loan_product)
        if application.loan_product != None:
            Survey.objects.filter(application=application).delete()
        application.loan_product = loan_product
        application.save()
        return 200, payload

    @route.get('/loan-product/{application_id}', response={200: GetLoanProductSchema, 404: ErrorMessage}, auth=JWTAuth())
    def get_loan_product(self, application_id: int):
        application = get_object_or_404(Application, id=application_id)
        loan_product = application.loan_product
        if loan_product is None:
            return 404, {"message": "application does not have loan product"}
        return 200, loan_product
