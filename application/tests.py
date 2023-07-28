from decouple import config
from django.test import TestCase, Client
from ninja_jwt.tokens import RefreshToken

from account.models import User
from applicant.models import Applicant
from datetime import date

from applicant.tests import AuthTestCase
from loanproduct.models import LoanProduct
from .models import Application, ApplicantCustomColumn, Collateral
from .api import ApplicantDetailController

class ApplicationModelTest(TestCase):

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
        self.application = Application.objects.create(
            applicant = self.applicant,
            amount = 1000000,
            tenure = 365,
            interest_rate = 12,
            interest_type = "Flat",
            usage_type = "Konsumsi",
        )
    
    def test_amount_field(self):
        self.assertEqual(self.application.amount, 1000000)

    def test_tenure_field(self):
        self.assertEqual(self.application.tenure, 365)

    def test_interest_rate_field(self):
        self.assertEqual(self.application.interest_rate, 12)

    def test_interest_type_field(self):
        self.assertEqual(self.application.interest_type, "Flat")

    def test_usage_type_field(self):
        self.assertEqual(self.application.usage_type, "Konsumsi")
    
    def test_str_function(self):
        self.assertEqual(str(self.application.amount), str(self.application))

class CollateralModelTest(TestCase):
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
        self.application = Application.objects.create(
            applicant = self.applicant,
            amount = 1000000,
            tenure = 365,
            interest_rate = 12,
            interest_type = "Flat",
            usage_type = "Konsumsi",
        )
        self.collateral = Collateral.objects.create(
            application = self.application,
            collateral_type = "Mobil",
            collateral_value = 1,
        )
    
    def test_collateral_type_field(self):
        self.assertEqual(self.collateral.collateral_type, "Mobil")
    
    def test_collateral_value_field(self):
        self.assertEqual(self.collateral.collateral_value, 1)

    def test_str_function(self):
        self.assertEqual(self.collateral.collateral_type, str(self.collateral))

class ApplicantCustomColumnModelTest(TestCase):
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
        self.applicant_custom_column = ApplicantCustomColumn.objects.create(
            applicant = self.applicant,
            column_name = "Hobi",
            column_value = "Mengeluh seperti pemuda jaman sekarang"
        )
    
    def test_column_name_field(self):
        self.assertEqual(self.applicant_custom_column.column_name, "Hobi")

    def test_column_value_field(self):
        self.assertEqual(self.applicant_custom_column.column_value, "Mengeluh seperti pemuda jaman sekarang")
    
    def test_str_function(self):
        self.assertEqual(str(self.applicant_custom_column), "Hobi: Mengeluh seperti pemuda jaman sekarang")
    

class ApplicantDetailControllerTest(AuthTestCase):

    @classmethod
    def setUpClass(cls):
        super(ApplicantDetailControllerTest, cls).setUpClass()
        cls.APPLICANT_BASE_ENDPOINT = "/api/applicant"
        cls.JSON_CONTENT_TYPE = "application/json"
        cls.controller = ApplicantDetailController()
        cls.client = Client(cls.controller)
        cls.payload = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"4",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000"
        }
        cls.payload_with_application = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"4",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000",
            "application":{
                "amount": "1000000",
                "usage_type": "Konsumsi"
            }
        }
        cls.payload_with_application_collateral = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"4",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000",
            "application":{
                "amount": "1000000",
                "usage_type": "Konsumsi"
            },
            "collateral":{
                "collateral_type": "Mobil",
                "collateral_value": "100000000"
            }
        }
        cls.payload2 = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"4",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000"
        }
        cls.payload_put = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"5",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000",
            "application_status":"Accepted"
        }
        cls.payload_put_rejected = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"5",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000",
            "application_status":"Rejected"
        }

        cls.payload_put_change_on_basic_data = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567891", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"4",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000"
        }

        cls.payload_put_add_custom_column = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"4",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000",
            "custom_columns": [
                {
                    "column_name" : "Custom Column Name",
                    "column_value" : "Custom Column Value"
                }
            ]
        }

        cls.payload_put_edit_custom_column_value = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"4",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000",
            "custom_columns": [
                {
                    "column_name" : "Custom Column Name",
                    "column_value" : "Custom Column Value Changed"
                }
            ]
        }

        cls.payload_put_delete_custom_column_value = {
            "fullname":"John Doe", "surname": "John", "gender":"Male", 
            "birth_place":"Jakarta", "birth_date":"2000-01-01", "mother_maiden_name":"Doe", 
            "phone_number":"08123456789", "email":"john.doe@example.com",
            "identity_number":"1234567890", "tax_number":"081785542123321",
            "religion":"Islam", "marital_status":"Kawin",
            "dependants_count":"4",
            "domicile_address":"Jl. Sudirman", "domicile_subdistrict":"Kebayoran Lama",
            "domicile_district":"Jakarta Selatan", "domicile_city":"Jakarta", "domicile_postal_code":"12345",
            "identity_address":"Jl. Namridus", "identity_subdistrict":"Naroyabek Amal ",
            "identity_district":"Atrakaj Natales", "identity_city":"Atrakaj", "identity_postal_code":"54321",
            "occupation":"PNS", "office_name":"Universitas Belajar", "office_address":"Jl. Belajar Rajin No.5",
            "office_business_type":"Pendidikan", "office_department":"Gol.IV", "office_phone_number":"021123456",
            "annual_income":"60000000",
            "custom_columns": []
        }

        cls.applicant = Applicant.objects.create(
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

        cls.application = Application.objects.create(
            applicant = cls.applicant,
            amount = 1000000,
            tenure = 365,
            interest_rate = 12,
            interest_type = "Flat",
            usage_type = "Konsumsi",
        )

        cls.loan_product = LoanProduct.objects.create(
            name="Test Loan Product",
            description="Test Loan Product Description",
            category="Test Loan Product Category",
        )

    def test_create_applicant_successful(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload,
            content_type=self.JSON_CONTENT_TYPE
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("applicant_id", response.json())
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        self.assertEqual(applicant.identity_number, "1234567890")

    def test_create_applicant_successful_with_application(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload_with_application,
            content_type=self.JSON_CONTENT_TYPE
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("applicant_id", response.json())
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        application = Application.objects.get(applicant=applicant)
        self.assertEqual(str(application), "1000000")
        self.assertEqual(application.usage_type, "Konsumsi")

    def test_create_applicant_successful_with_application_collateral(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload_with_application_collateral,
            content_type=self.JSON_CONTENT_TYPE
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("applicant_id", response.json())
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        application = Application.objects.get(applicant=applicant)
        collateral = Collateral.objects.get(application=application)
        self.assertEqual(collateral.collateral_type, "Mobil")
        self.assertEqual(collateral.collateral_value, 100000000)

    def test_create_duplicate_applicant_unsuccessful(self):
        self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload,
            content_type=self.JSON_CONTENT_TYPE
        )
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload,
            content_type=self.JSON_CONTENT_TYPE
        )
        self.assertEqual(response.status_code, 409)
        self.assertIn("Applicant already exists", response.json().values())
    
    def test_get_applicant_successful(self):
        applicant = Applicant.objects.create(**self.payload)
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['identity_number'], "1234567890")
    
    def test_get_applicant_successful_with_application(self):
        applicant = Applicant.objects.create(**self.payload)
        application = Application.objects.create(applicant=applicant, amount=1000000, tenure=0, interest_type="", interest_rate=0, usage_type="")
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("application", str(response.json().keys()))
        self.assertEqual(response.json()["application"]["amount"], 1000000)

    def test_get_applicant_successful_with_application_and_collateral(self):
        applicant = Applicant.objects.create(**self.payload)
        application = Application.objects.create(applicant=applicant, amount=1000000, tenure=0, interest_type="", interest_rate=0, usage_type="")
        Collateral.objects.create(application=application, collateral_type="Mobil", collateral_value=1000000)
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("application", str(response.json().keys()))
        self.assertEqual(response.json()["application"]["amount"], 1000000)
        self.assertIn("collateral", str(response.json().keys()))
        self.assertEqual(response.json()["collateral"]["collateral_type"], "Mobil")
    
    def test_get_non_exist_applicant_return_not_found_message(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT+"/999",
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Applicant does not exist", response.json().values())
    
    def test_update_applicant_successful(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload2,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        old_applicant_dependants_count = str(applicant.dependants_count)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        applicant = Applicant.objects.get(id=applicant_id)
        new_applicant_dependants_count = str(applicant.dependants_count)
        self.assertNotEqual(old_applicant_dependants_count, new_applicant_dependants_count)
        self.assertEqual(new_applicant_dependants_count, "5")

    def test_update_applicant_status_accepted_successful(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload2,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        old_applicant_status = applicant.application_status
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        applicant = Applicant.objects.get(id=applicant_id)
        new_applicant_status = applicant.application_status
        self.assertNotEqual(old_applicant_status, new_applicant_status)
        self.assertEqual(new_applicant_status, "Accepted")

    def test_update_applicant_status_rejected_successful(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload2,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        old_applicant_status = applicant.application_status
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put_rejected,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        applicant = Applicant.objects.get(id=applicant_id)
        new_applicant_status = applicant.application_status
        self.assertNotEqual(old_applicant_status, new_applicant_status)
        self.assertEqual(new_applicant_status, "Rejected")
    
    def test_update_non_exist_applicant_return_not_found_message(self):
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/999",
            self.payload_put,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Applicant does not exist", response.json().values())

    def test_update_applicant_basic_data_unsuccessful(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT,
            self.payload2,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        old_applicant_identity_number = str(applicant.identity_number)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put_change_on_basic_data,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("Forbidden to update applicant basic data", response.json().values())
        applicant = Applicant.objects.get(id=applicant_id)
        new_applicant_identity_number = str(applicant.identity_number)
        self.assertEqual(old_applicant_identity_number, new_applicant_identity_number)

    def test_update_applicant_add_custom_column(self):
        applicant = Applicant.objects.create(**self.payload)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put_add_custom_column,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        applicant_custom_column = ApplicantCustomColumn.objects.get(applicant=applicant, column_name="Custom Column Name")
        self.assertNotEqual(applicant_custom_column, None)
        self.assertEqual(applicant_custom_column.column_value, "Custom Column Value")
    
    def test_update_applicant_edit_by_delete_custom_column(self):
        applicant = Applicant.objects.create(**self.payload)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put_add_custom_column,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        applicant_custom_columns = ApplicantCustomColumn.objects.filter(applicant=applicant)
        old_custom_column_counts = len(applicant_custom_columns)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put_delete_custom_column_value,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant = Applicant.objects.get(id=applicant_id)
        applicant_custom_columns = ApplicantCustomColumn.objects.filter(applicant=applicant)
        new_custom_column_counts = len(applicant_custom_columns)
        self.assertNotEqual(old_custom_column_counts, new_custom_column_counts)
        
    def test_update_applicant_with_application_and_collateral(self):
        applicant = Applicant.objects.create(**self.payload)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put_add_custom_column,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_with_application_collateral,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        application = Application.objects.get(applicant=applicant)
        collateral = Collateral.objects.get(application=application)
        self.assertEqual(collateral.collateral_type, "Mobil")
        self.assertEqual(collateral.collateral_value, 100000000)
    
    def test_update_applicant_edit_custom_column_value(self):
        applicant = Applicant.objects.create(**self.payload)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put_add_custom_column,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant_id = response.json()['applicant_id']
        applicant = Applicant.objects.get(id=applicant_id)
        applicant_custom_column = ApplicantCustomColumn.objects.get(applicant=applicant, column_name="Custom Column Name")
        old_custom_column_value = str(applicant_custom_column.column_value)
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            self.payload_put_edit_custom_column_value,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        applicant = Applicant.objects.get(id=applicant_id)
        applicant_custom_column = ApplicantCustomColumn.objects.get(applicant=applicant, column_name="Custom Column Name")
        new_custom_column_value = str(applicant_custom_column.column_value)
        self.assertNotEqual(old_custom_column_value, new_custom_column_value)
        self.assertEqual(new_custom_column_value, "Custom Column Value Changed")

    def test_get_applicant_with_custom_columns(self):
        applicant = Applicant.objects.create(**self.payload)
        applicant_custom_column = ApplicantCustomColumn.objects.create(
            applicant = applicant,
            column_name = "Ayayaya",
            column_value = "Ayaya!"
        )
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT+"/"+str(applicant.id),
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("custom_columns", response.json())
        custom_column1 = response.json()['custom_columns'][0]
        self.assertEqual(custom_column1["column_name"], "Ayayaya")
        self.assertEqual(custom_column1["column_value"], "Ayaya!")
        
    def test_set_loan_product(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT+"/loan-product/"+str(self.application.id),
            {
                "loan_product_id": self.loan_product.id
            },
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_set_loan_product_applicant_not_found(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT+"/loan-product/999",
            {
                "loan_product_id": self.loan_product.id
            },
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_get_loan_product(self):
        self.application.loan_product = self.loan_product
        self.application.save()
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT+"/loan-product/"+str(self.application.id),
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.loan_product.id)

    def test_get_loan_product_applicant_not_found(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT+"/loan-product/999",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_get_loan_product_not_created(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT+"/loan-product/"+str(self.application.id),
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        