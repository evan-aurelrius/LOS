from datetime import date
from unittest.mock import patch, MagicMock

from decouple import config
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.utils import timezone
from django.utils.datetime_safe import strftime
from ninja_jwt.tokens import RefreshToken

from account.models import User
from .api import ApplicantController
from .models import Applicant, ApplicantFile


class AuthTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(AuthTestCase, cls).setUpClass()
        cls.admin = User.objects.create_user(email="firstAdmin@admin.com", password=config("test_admin_password"))
        cls.refresh = RefreshToken.for_user(user=cls.admin)
        cls.pair_token = {
            "refresh": str(cls.refresh),
            "access": str(cls.refresh.access_token)
        }
        cls.auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + cls.pair_token["access"],
        }
        cls.admin_cabang = User.objects.create_user(email="cabang@admin.com", password="cabang", branch="Cabang")
        cls.refresh_cabang = RefreshToken.for_user(user=cls.admin_cabang)
        cls.pair_token_cabang = {
            "refresh": str(cls.refresh_cabang),
            "access": str(cls.refresh_cabang.access_token)
        }
        cls.auth_headers_cabang = {
            "HTTP_AUTHORIZATION": "Bearer " + cls.pair_token_cabang["access"],
        }

class ApplicantModelTest(TestCase):

    def setUp(self):
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
            annual_income=100000000,
            branch="Pusat"
        )

    def test_fullname_field(self):
        self.assertEqual(self.applicant.fullname, "Dohn Joe")

    def test_surname_field(self):
        self.assertEqual(self.applicant.surname, "Joe")

    def test_create_date_field(self):
        self.assertEqual(self.applicant.create_date, date(2020, 1, 1))

    def test_application_status_field(self):
        self.assertEqual(self.applicant.application_status, "Pending")

    def test_gender_field(self):
        self.assertEqual(self.applicant.gender, "Laki-laki")

    def test_birth_place_field(self):
        self.assertEqual(self.applicant.birth_place, "Jakarta")

    def test_birth_date_field(self):
        self.assertEqual(self.applicant.birth_date, date(1980, 1, 1))

    def test_mother_maiden_name_field(self):
        self.assertEqual(self.applicant.mother_maiden_name, "Mary")

    def test_phone_number_field(self):
        self.assertEqual(self.applicant.phone_number, "08123456789")

    def test_email_field(self):
        self.assertEqual(self.applicant.email, "dohn.joe@example.com")

    def test_identity_number_field(self):
        self.assertEqual(self.applicant.identity_number, "123456789")

    def test_tax_number_field(self):
        self.assertEqual(self.applicant.tax_number, "987654321")

    def test_religion_field(self):
        self.assertEqual(self.applicant.religion, "Islam")

    def test_marital_status_field(self):
        self.assertEqual(self.applicant.marital_status, "Kawin")

    def test_dependants_count_field(self):
        self.assertEqual(self.applicant.dependants_count, 2)

    def test_domicile_address_field(self):
        self.assertEqual(self.applicant.domicile_address, "Jl. Sudirman No. 123")

    def test_domicile_subdistrict_field(self):
        self.assertEqual(self.applicant.domicile_subdistrict, "Karet Semanggi")

    def test_domicie_district_field(self):
        self.assertEqual(self.applicant.domicile_district, "Setiabudi")

    def test_domicile_city_field(self):
        self.assertEqual(self.applicant.domicile_city, "Jakarta Selatan")

    def test_domicile_postal_code_field(self):
        self.assertEqual(self.applicant.domicile_postal_code, "12920")

    def test_occupation(self):
        self.assertEqual(self.applicant.occupation, "Programmer")

    def test_office_name(self):
        self.assertEqual(self.applicant.office_name, "PT Example")

    def test_office_address(self):
        self.assertEqual(self.applicant.office_address, "Jl. Gatot Subroto No. 789")

    def test_office_business_type(self):
        self.assertEqual(self.applicant.office_business_type, "IT")

    def test_office_department(self):
        self.assertEqual(self.applicant.office_department, "Engineering")

    def test_office_phone_number(self):
        self.assertEqual(self.applicant.office_phone_number, "02198765432")

    def test_annual_income(self):
        self.assertEqual(self.applicant.annual_income, 100000000)

    def test_branch(self):
        self.assertEqual(self.applicant.branch, "Pusat")

    def test_applicant_str_method(self):
        self.assertEqual(str(self.applicant), self.applicant.fullname)


class ApplicantListTestCase(AuthTestCase):

    @classmethod
    def setUpClass(cls):
        super(ApplicantListTestCase, cls).setUpClass()
        cls.controller = ApplicantController()
        cls.client = Client(cls.controller)

        cls.applicant1 = Applicant.objects.create(fullname="John Doe",
                                                  create_date="2020-01-01",
                                                  application_status="Pending",
                                                  gender="Male",
                                                  birth_place="Jakarta",
                                                  birth_date="2000-01-01",
                                                  mother_maiden_name="Doe",
                                                  phone_number="08123456789",
                                                  email="john.doe@example.com",
                                                  identity_number="1234567890",
                                                  domicile_address="Jl. Sudirman",
                                                  domicile_subdistrict="Kebayoran Lama",
                                                  domicile_district="Jakarta Timur",
                                                  domicile_city="Jakarta",
                                                  domicile_postal_code="12345")

        cls.applicant2 = Applicant.objects.create(fullname="Jane Smith",
                                                  create_date="2020-01-02",
                                                  application_status="Pending",
                                                  gender="Female",
                                                  birth_place="Bandung",
                                                  birth_date="2000-01-02",
                                                  mother_maiden_name="Smith",
                                                  phone_number="08234567891",
                                                  email="jane.smith@example.com",
                                                  identity_number="0987654321",
                                                  domicile_address="Jl. Thamrin",
                                                  domicile_subdistrict="Menteng",
                                                  domicile_district="Jakarta Pusat",
                                                  domicile_city="Jakarta",
                                                  domicile_postal_code="54321")

        cls.applicant3 = Applicant.objects.create(fullname="Jane Doe",
                                                  create_date="2020-01-03",
                                                  application_status="Rejected",
                                                  gender="Female",
                                                  birth_place="Tangerang",
                                                  birth_date="2000-01-03",
                                                  mother_maiden_name="Doe",
                                                  phone_number="08234567892",
                                                  email="jane.doe@example.com",
                                                  identity_number="0987654322",
                                                  domicile_address="Jl. Imam Bonjol",
                                                  domicile_subdistrict="Karawaci",
                                                  domicile_district="Sukajadi",
                                                  domicile_city="Tangerang",
                                                  domicile_postal_code="54322")

        cls.applicant4 = Applicant.objects.create(fullname="Joe Smith",
                                                  create_date="2020-01-04",
                                                  application_status="Accepted",
                                                  gender="Male",
                                                  birth_place="Solo",
                                                  birth_date="2000-01-04",
                                                  mother_maiden_name="Smith",
                                                  phone_number="08234567893",
                                                  email="joe.smith@example.com",
                                                  identity_number="0987654323",
                                                  domicile_address="Jl. Merdeka",
                                                  domicile_subdistrict="Citarum",
                                                  domicile_district="Citarum",
                                                  domicile_city="Bandung",
                                                  domicile_postal_code="54324")

    def test_list_applicant(self):
        response = self.client.get("/api/applicant/list", **self.auth_headers)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["count"], 4)
        self.assertEqual(len(response.json()["items"]), 4)

        item1, item2, item3, item4 = response.json()["items"]

        self.assertEqual(item1["id"], self.applicant1.id)
        self.assertEqual(item1["fullname"], "John Doe")
        self.assertEqual(item1["application_status"], "Pending")
        self.assertEqual(item1["create_date"], "2020-01-01")

        self.assertEqual(item2["id"], self.applicant2.id)
        self.assertEqual(item2["fullname"], "Jane Smith")
        self.assertEqual(item2["application_status"], "Pending")
        self.assertEqual(item2["create_date"], "2020-01-02")

        self.assertEqual(item3["id"], self.applicant3.id)
        self.assertEqual(item3["fullname"], "Jane Doe")
        self.assertEqual(item3["application_status"], "Rejected")
        self.assertEqual(item3["create_date"], "2020-01-03")

        self.assertEqual(item4["id"], self.applicant4.id)
        self.assertEqual(item4["fullname"], "Joe Smith")
        self.assertEqual(item4["application_status"], "Accepted")
        self.assertEqual(item4["create_date"], "2020-01-04")

    def test_list_applicant_pagination(self):
        response = self.client.get("/api/applicant/list?limit=2&offset=2", **self.auth_headers)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["count"], 4)
        self.assertEqual(len(response.json()["items"]), 2)

        item1, item2 = response.json()["items"]

        self.assertEqual(item1["id"], self.applicant3.id)
        self.assertEqual(item2["id"], self.applicant4.id)

    def test_list_applicant_filter_by_application_status(self):
        response = self.client.get("/api/applicant/list?status=Accepted", **self.auth_headers)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["items"]), 1)

        item1 = response.json()["items"][0]

        self.assertEqual(item1["id"], self.applicant4.id)

    def test_list_applicant_filter_by_date_range(self):
        response = self.client.get("/api/applicant/list?start_date=02-01-2020&end_date=03-01-2020", **self.auth_headers)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(len(response.json()["items"]), 2)

        item1, item2 = response.json()["items"]

        self.assertEqual(item1["id"], self.applicant2.id)
        self.assertEqual(item2["id"], self.applicant3.id)

    def test_list_applicant_filter_by_date_range_invalid_start_date(self):
        response = self.client.get("/api/applicant/list?start_date=2020-01-02&end_date=03-01-2020", **self.auth_headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid start date format. Use DD-MM-YYYY.")

    def test_list_applicant_filter_by_date_range_invalid_end_date(self):
        response = self.client.get("/api/applicant/list?start_date=02-01-2020&end_date=2020-01-03", **self.auth_headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid end date format. Use DD-MM-YYYY.")

    def test_list_applicant_filter_by_domicile_city(self):
        response = self.client.get("/api/applicant/list?area=Tangerang", **self.auth_headers)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["items"]), 1)

        item1 = response.json()["items"][0]

        self.assertEqual(item1["id"], self.applicant3.id)

    def test_list_applicant_filter_by_multiple_conditions(self):
        response = self.client.get(
            "/api/applicant/list?status=Pending&start_date=02-01-2020&end_date=03-01-2020&area=Jakarta",
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["items"]), 1)

        item1 = response.json()["items"][0]

        self.assertEqual(item1["id"], self.applicant2.id)

    def test_list_applicant_cabang(self):
        response = self.client.get("/api/applicant/list", **self.auth_headers_cabang)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["count"], 0)
        self.assertEqual(len(response.json()["items"]), 0)


class ApplicantFileTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ApplicantFileTestCase, cls).setUpClass()
        cls.controller = ApplicantController()
        cls.client = Client(cls.controller)
        cls.admin = User.objects.create_user(email="firstAdmin@admin.com", password=config("test_admin_password"), first_name="Admin", last_name="Sama")
        cls.refresh = RefreshToken.for_user(user=cls.admin)
        cls.pair_token = {
            "refresh": str(cls.refresh),
            "access": str(cls.refresh.access_token)
        }
        cls.auth_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {cls.pair_token['access']}",
        }

        cls.applicant = Applicant.objects.create(fullname="Applicant",
                                                 create_date="2002-02-02",
                                                 application_status="Pending",
                                                 gender="Male",
                                                 birth_place="Place",
                                                 birth_date="2001-01-01",
                                                 mother_maiden_name="Mother",
                                                 phone_number="08888888",
                                                 email="email@email.com",
                                                 identity_number="1111111",
                                                 domicile_address="Address",
                                                 domicile_subdistrict="Subdistrict",
                                                 domicile_district="District",
                                                 domicile_city="City",
                                                 domicile_postal_code="11111")

        cls.file = SimpleUploadedFile("file.txt", b"file_content")
        cls.detail = "KTP"

    @patch.object(default_storage, 'save', MagicMock(return_value='applicant_files/1/file.txt'))
    def test_upload_applicant_file(self):
        response = self.client.post(f"/api/applicant/{self.applicant.id}/file", data={'files': [self.file], 'detail': self.detail}, **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Files successfully uploaded"})
        self.assertTrue(ApplicantFile.objects.filter(applicant=self.applicant).exists())

    @patch.object(default_storage, 'save', MagicMock(return_value='applicant_files/1/file.txt'))
    def test_get_applicant_file_list(self):
        self.client.post(f"/api/applicant/{self.applicant.id}/file", data={'files': [self.file], 'detail': self.detail}, **self.auth_headers)
        response = self.client.get(f"/api/applicant/{self.applicant.id}/file/list", **self.auth_headers)
        applicant_file = ApplicantFile.objects.filter(applicant=self.applicant).first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], str(applicant_file.id))
        self.assertEqual(response.json()[0]['name'], applicant_file.filename)
        self.assertEqual(response.json()[0]['extension'], applicant_file.extension)
        self.assertEqual(response.json()[0]['url'], applicant_file.file.url)
        self.assertEqual(response.json()[0]['detail'], applicant_file.detail)

    @patch.object(default_storage, 'save', MagicMock(return_value='applicant_files/1/file.txt'))
    def test_delete_applicant_file(self):
        self.client.post(f"/api/applicant/{self.applicant.id}/file", data={'files': [self.file], 'detail': self.detail}, **self.auth_headers)
        applicant_file = ApplicantFile.objects.filter(applicant=self.applicant).first()
        response = self.client.delete(f"/api/applicant/file/{applicant_file.id}", **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": f"{applicant_file.filename} successfully deleted"})
        self.assertFalse(ApplicantFile.objects.filter(id=applicant_file.id).exists())

    @patch.object(default_storage, 'save', MagicMock(return_value='applicant_files/1/file.txt'))
    def test_get_applicant_update_log(self):
        applicant = Applicant.objects.get(id=self.applicant.id)
        old_applicant_update_date = applicant.update_date
        response = self.client.post(f"/api/applicant/{self.applicant.id}/file", data={'files': [self.file], 'detail': self.detail}, **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        applicant = Applicant.objects.get(id=self.applicant.id)
        new_applicant_update_date = applicant.update_date
        response = self.client.get(
            f"/api/applicant/log/{self.applicant.id}",
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(old_applicant_update_date, new_applicant_update_date)
        self.assertEqual(response.json()["update_date"], strftime(timezone.localtime(new_applicant_update_date), "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(response.json()["update_by"], f"{self.admin.first_name} {self.admin.last_name}")