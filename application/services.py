from application.models import Applicant, Application, Collateral, ApplicantCustomColumn

class ApplicantDetailService:

    @classmethod
    def create_applicant(*post_payload):
        applicant = Applicant.objects.create(**(post_payload[1]))
        return applicant
    
    @staticmethod
    def update_applicant(applicant, put_payload):
        for attr, value in put_payload.items():
            setattr(applicant, attr, value)
        applicant.save()

    
class ApplicationService:

    @staticmethod
    def create_application(applicant, amount, usage_type, tenure, interest_rate, interest_type):
        application = Application.objects.create(applicant=applicant, amount=amount, tenure=tenure, interest_rate=interest_rate, interest_type=interest_type, usage_type=usage_type)
        return application
    
    @staticmethod
    def get_application(applicant):
        application = None
        try:
            application = Application.objects.get(applicant=applicant)
        except Application.DoesNotExist:
            application = None
        return application
    
    @staticmethod
    def update_or_create_application(applicant, application_update):
        application = None
        if application_update != "Null":
            try:
                application = Application.objects.get(applicant=applicant)
            except Application.DoesNotExist:
                application = ApplicationService.create_application(applicant, application_update["amount"], application_update["usage_type"], application_update["tenure"], application_update["interest_rate"], application_update["interest_type"])
            finally:
                application.amount = application_update["amount"]
                application.tenure = application_update["tenure"]
                application.usage_type = application_update["usage_type"]
                application.interest_rate = application_update["interest_rate"]
                application.interest_type = application_update["interest_type"]
                application.save()
        return application

class CollateralService:

    @staticmethod
    def create_collateral(application, collateral_type, collateral_value):
        collateral = Collateral.objects.create(application=application, collateral_type=collateral_type, collateral_value=collateral_value)
        return collateral

    @staticmethod
    def get_collateral(application):
        collateral = None
        try:
            collateral = Collateral.objects.get(application=application)
        except Collateral.DoesNotExist:
            collateral = None
        return collateral

    @staticmethod
    def update_or_create_collateral(application, collateral_update):
        collateral = None
        if collateral_update != "Null":
            try:
                collateral = Collateral.objects.get(application=application)
            except Collateral.DoesNotExist:
                collateral = CollateralService.create_collateral(application, collateral_update["collateral_type"], collateral_update["collateral_value"])
            finally:
                collateral.collateral_type = collateral_update["collateral_type"]
                collateral.collateral_value = collateral_update["collateral_value"]
                collateral.save()
        return collateral 

class ApplicantCustomColumnService:

    @staticmethod
    def get_all_applicant_custom_column(applicant):
        applicant_custom_columns = ApplicantCustomColumn.objects.filter(applicant=applicant)
        return applicant_custom_columns
    
    @staticmethod
    def update_or_create_applicant_custom_columns(applicant, custom_column_updates):
        for custom_column_update in custom_column_updates:
            try:
                applicant_custom_column = ApplicantCustomColumn.objects.get(applicant=applicant, column_name=custom_column_update['column_name'])
            except ApplicantCustomColumn.DoesNotExist:
                applicant_custom_column = ApplicantCustomColumn.objects.create(applicant=applicant, column_name=custom_column_update['column_name'], column_value="")
            finally:
                applicant_custom_column.column_value = custom_column_update['column_value']
                applicant_custom_column.save()
    
    @staticmethod
    def delete_applicant_custom_columns_not_in_update(applicant, custom_column_updates):
        custom_column_update_names = []
        for custom_column_update in custom_column_updates:
            custom_column_update_names.append(custom_column_update["column_name"])
        applicant_custom_columns = ApplicantCustomColumn.objects.filter(applicant=applicant)
        for applicant_custom_column in applicant_custom_columns:
            if applicant_custom_column.column_name not in custom_column_update_names:
                applicant_custom_column.delete()
        