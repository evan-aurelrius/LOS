from django.test import TestCase
from django.test import Client
from decouple import config
from applicant.models import Applicant
from loanproduct.models import LoanProduct, LoanProductSection
from .models import Answer
from question.models import Question
from account.models import User
from ninja_jwt.tokens import RefreshToken
from application.models import Application
from survey.models import Survey
from section.models import Section
from unittest.mock import MagicMock
from datetime import date
FIRST_ADMIN = "first admin"
NOT_ADMIN = "not admin"
FIRST_SU = "first_su"
NOT_SU = "not_su"


class AnswerModelTest(TestCase):

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
        self.answer = Answer.objects.create(
            survey=self.survey,
            question=self.question.question,
            chosen="Red",
            score=1
        )

    def testCreateAnswer(self):
        saved_answers = Answer.objects.all()
        self.assertEqual(saved_answers.count(), 1)
        self.assertEqual(saved_answers[0].chosen, "Red")
        self.assertEqual(saved_answers[0].score, 1)
        self.assertEqual(saved_answers[0].question, self.question.question)
        self.assertEqual(saved_answers[0].survey, self.survey)

    def testCreateAnswerNegative(self):
        saved_answers = Answer.objects.all()
        self.assertNotEqual(saved_answers.count(), 0)

    def testUpdateAnswer(self):
        self.answer.chosen = "Blue"
        self.answer.score = 2
        self.answer.save()
        saved_answers = Answer.objects.all()
        self.assertEqual(saved_answers.count(), 1)
        self.assertEqual(saved_answers[0].chosen, "Blue")
        self.assertEqual(saved_answers[0].score, 2)
        self.assertEqual(saved_answers[0].question, self.question.question)
        self.assertEqual(saved_answers[0].survey, self.survey)

    def testUpdateAnswerNegative(self):
        self.answer.chosen = "Blue"
        self.answer.score = 2
        self.answer.save()
        saved_answers = Answer.objects.all()
        self.assertEqual(saved_answers.count(), 1)
        self.assertNotEqual(saved_answers[0].chosen, "Red")
        self.assertNotEqual(saved_answers[0].score, 1)