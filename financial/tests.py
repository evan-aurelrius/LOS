from django.test import Client, TestCase
from account.models import User
from ninja_jwt.tokens import RefreshToken
from financial.api import FinancialController
from .models import Financial
from applicant.models import Applicant
from datetime import date
from decouple import config


class FinancialModelCase(TestCase):
    def setUp(self):
        self.applicant = Applicant.objects.create(
            fullname="Dohn Ayaya",
            surname="Ayaya",
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
        self.financial = Financial.objects.create(
            applicant=self.applicant,
            amount=1000000,
            title="Gaji",
        )

    def test_title_field(self):
        self.assertEqual(self.financial.title, "Gaji")

    def test_title_field_negative(self):
        self.assertNotEqual(self.financial.title, "Gaji 2")

    def test_amount_field(self):
        self.assertEqual(self.financial.amount, 1000000)

    def test_amount_field_negative(self):
        self.assertNotEqual(self.financial.amount, 2000000)

    def test_applicant_field(self):
        self.assertEqual(self.financial.applicant, self.applicant)

    def test_applicant_field_negative(self):
        self.assertNotEqual(self.financial.applicant, "Dohn Ayaya")


class FinancialApiTest(FinancialModelCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
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
        cls.APPLICANT_BASE_ENDPOINT = "/api/financial"
        cls.JSON_CONTENT_TYPE = "application/json"
        cls.controller = FinancialController()
        cls.payload = {
            "title": "Gaji",
            "amount": 1000000
        }

    def testCreateFinancial(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT + f"/create/{self.applicant.id}",
            data=self.payload,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 201)

    def testCreateFinancialNegative(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT + f"/create/1000",
            data=self.payload,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)

    def testListFinancial(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + f"/list/{self.applicant.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testListFinancialNegative(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + f"/list/1000",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertNotEqual(response.status_code, 404)

    def testUpdateFinancial(self):
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT + f"/{self.financial.id}",
            data=self.payload,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testUpdateFinancialNegative(self):
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT + f"/1000",
            data=self.payload,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)

    def testDeleteFinancial(self):
        response = self.client.delete(
            self.APPLICANT_BASE_ENDPOINT + f"/{self.financial.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testDeleteFinancialNegative(self):
        response = self.client.delete(
            self.APPLICANT_BASE_ENDPOINT + f"/1000",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)