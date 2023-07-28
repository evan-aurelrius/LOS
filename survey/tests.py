from django.test import TestCase
from django.test import Client
from decouple import config
from applicant.models import Applicant
from loanproduct.models import LoanProduct
from .models import Survey
from question.models import Question
from account.models import User
from ninja_jwt.tokens import RefreshToken
from application.models import Application
from survey.models import Survey
from section.models import Section
from datetime import date
from .api import SurveyController

FIRST_ADMIN = "first admin"
NOT_ADMIN = "not admin"
FIRST_SU = "first_su"
NOT_SU = "not_su"


class SurveyModelTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create(
            first_name=FIRST_ADMIN, email=FIRST_ADMIN, password=config('test_admin_password'))

        self.applicant = Applicant.objects.create(
            fullname="Dohn Joe",
            surname="Joe",
            create_date=date(2020, 1, 1),
            application_status="Pending",
            gender="Laki-laki",
            birth_place="Jakarta",
            birth_date=date(1980, 1, 1),
            mother_maiden_name="Mary",
            phone_number="08123456789",
            email="dohn.joe@example.com",
            identity_number="123456789",
            tax_number="987654321",
            religion="Islam",
            marital_status="Kawin",
            dependants_count=2,
            domicile_address="Jl. Sudirman No. 123",
            domicile_subdistrict="Karet Semanggi",
            domicile_district="Setiabudi",
            domicile_city="Jakarta Selatan",
            domicile_postal_code="12920",
            identity_address="Jl. Thamrin No. 456",
            identity_subdistrict="Menteng",
            identity_district="Jakarta Pusat",
            identity_city="Jakarta",
            identity_postal_code="10350",
            occupation="Programmer",
            office_name="PT Example",
            office_address="Jl. Gatot Subroto No. 789",
            office_business_type="IT",
            office_department="Engineering",
            office_phone_number="02198765432",
            annual_income=100000000
        )
        self.application = Application.objects.create(
            applicant=self.applicant,
            amount=1000000,
            tenure=365,
            interest_rate=12,
            interest_type="Flat",
            usage_type="Konsumsi",
        )
        self.DATETIME = "2010-10-10 10:10:10"
        self.loan_product = LoanProduct.objects.create(
            name="Asuransi Rumah",
            description="Houser",
            category="Default",
        )
        self.section = Section.objects.create(
            name="Ekonomi",
            minimum_score=10,
        )
        self.question = Question.objects.create(section=self.section, question="What is your name?", choices=[
            "John", "Jane", "Jack"], scores=[1, 2, 3])
        self.survey = Survey.objects.create(
            filler=self.admin,
            application=self.application,
            section=self.section,
            final_score=0
        )

    def testCreateSurvey(self):
        self.assertEqual(self.survey.filler, self.admin)
        self.assertEqual(self.survey.application, self.application)
        self.assertEqual(self.survey.section, self.section)
        self.assertEqual(self.survey.final_score, 0)

    def testCreateSurveyNegative(self):
        self.assertNotEqual(self.survey.filler, self.applicant)
        self.assertNotEqual(self.survey.application, self.loan_product)
        self.assertNotEqual(self.survey.section, self.question)
        self.assertNotEqual(self.survey.final_score, 1)


class SurveyApiTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = User.objects.create(
            first_name=FIRST_ADMIN, email=FIRST_ADMIN, password=config('test_admin_password'))

        cls.applicant = Applicant.objects.create(
            fullname="Dohn Joe",
            surname="Joe",
            create_date=date(2020, 1, 1),
            application_status="Pending",
            gender="Laki-laki",
            birth_place="Jakarta",
            birth_date=date(1980, 1, 1),
            mother_maiden_name="Mary",
            phone_number="08123456789",
            email="dohn.joe@example.com",
            identity_number="123456789",
            tax_number="987654321",
            religion="Islam",
            marital_status="Kawin",
            dependants_count=2,
            domicile_address="Jl. Sudirman No. 123",
            domicile_subdistrict="Karet Semanggi",
            domicile_district="Setiabudi",
            domicile_city="Jakarta Selatan",
            domicile_postal_code="12920",
            identity_address="Jl. Thamrin No. 456",
            identity_subdistrict="Menteng",
            identity_district="Jakarta Pusat",
            identity_city="Jakarta",
            identity_postal_code="10350",
            occupation="Programmer",
            office_name="PT Example",
            office_address="Jl. Gatot Subroto No. 789",
            office_business_type="IT",
            office_department="Engineering",
            office_phone_number="02198765432",
            annual_income=100000000
        )
        cls.application = Application.objects.create(
            applicant=cls.applicant,
            amount=1000000,
            tenure=365,
            interest_rate=12,
            interest_type="Flat",
            usage_type="Konsumsi",
        )
        cls.DATETIME = "2010-10-10 10:10:10"
        cls.loan_product = LoanProduct.objects.create(
            name="Asuransi Rumah",
            description="Houser",
            category="Default",
        )
        cls.section = Section.objects.create(
            name="Ekonomi",
            minimum_score=10,
        )
        cls.question = Question.objects.create(section=cls.section, question="What is your name?", choices=[
            "John", "Jane", "Jack"], scores=[1, 2, 3])
        cls.survey = Survey.objects.create(
            filler=cls.admin,
            application=cls.application,
            section=cls.section,
            final_score=0
        )

        cls.client = Client()
        cls.APPLICANT_BASE_ENDPOINT = "/api/survey"
        cls.JSON_CONTENT_TYPE = "application/json"
        cls.controller = SurveyController()
        cls.admin = User.objects.create_user(
            email="firstAdmin@admin.com", password=config("test_admin_password"))
        cls.refresh = RefreshToken.for_user(user=cls.admin)
        cls.pair_token = {
            "refresh": str(cls.refresh),
            "access": str(cls.refresh.access_token)
        }
        cls.auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + cls.pair_token["access"],
        }
        cls.payload = {
            "application_id": cls.application.id,
            "section_id": cls.section.id,
            "answers": [
                {
                    "question": cls.question.id,
                    "chosen": "Jane"
                },
            ]
        }

    def testCreateSurvey(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            data=self.payload,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testCreateSurveyNegative(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            data=self.payload,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertNotEqual(response.status_code, 404)

    def testGetRemark(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + f"/remark/{self.application.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testGetRemarkNegative(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + f"/remark/999999",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def testGetSurvey(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + f"/{self.application.id}/{self.section.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testGetSurveyNegative(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + f"/{self.application.id}/{self.section.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertNotEqual(response.status_code, 404)

    def testGetSurveys(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + f"/{self.application.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testGetSurveysNegative(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + f"/{self.application.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertNotEqual(response.status_code, 404)