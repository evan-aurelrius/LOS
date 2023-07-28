from datetime import date
from django.test import TestCase
from account.models import User
from applicant.models import Applicant
from application.models import Application
from comment.models import Comment
from django.core.files.uploadedfile import SimpleUploadedFile
from decouple import config


FIRST_ADMIN = "first admin"
NOT_ADMIN = "not admin"
FIRST_SU = "first_su"
NOT_SU = "not_su"


class CommentTestCase(TestCase):

    def setUp(self):
        self.admin = User.objects.create(
            first_name=FIRST_ADMIN, email=FIRST_ADMIN, password=config('test_admin_password'))
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
            applicant=self.applicant,
            amount=1000000,
            tenure=365,
            interest_rate=12,
            interest_type="Flat",
            usage_type="Konsumsi",
        )
        self.comment = Comment.objects.create(
            title="Test Title",
            message="Test Message",
            author_id=self.admin.id,
            application_id=self.application.id,
            attachment=SimpleUploadedFile("file.txt", b"file_content")
        )

    def test_comment_has_title(self):
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.title, self.comment.title)

    def test_comment_has_message(self):
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.message, self.comment.message)

    def test_comment_has_author(self):
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.author_id, self.comment.author_id)

    def test_comment_has_application(self):
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.application_id, self.comment.application_id)

    def test_comment_has_attachment(self):
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.attachment, self.comment.attachment)
