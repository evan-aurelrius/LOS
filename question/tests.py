from django.test import TestCase
from django.test import Client
from decouple import config

from applicant.tests import AuthTestCase
from section.models import Section
from .models import Question
from .api import QuestionController
from account.models import User
from ninja_jwt.tokens import RefreshToken
import json

DATETIME = "2010-10-10 10:10:10"
QUESTION = "What is your name?"
QUESTION_2 = "What is your favorite color?"
class QuestionModelTest(TestCase):
    def setUp(self):
        self.section = Section.objects.create(
            name="Section",
            minimum_score=10,
            create_date=DATETIME,
            update_date=DATETIME
        )

    def testCreateQuestion(self):
        question = Question.objects.create(section=self.section, question=QUESTION, choices=[
                                           "John", "Jane", "Jack"], scores=[1, 2, 3])
        self.assertEqual(question.question, QUESTION)
        self.assertEqual(question.choices, ["John", "Jane", "Jack"])
        self.assertEqual(question.scores, [1, 2, 3])

    def testCreateQuestionNegative(self):
        question = Question.objects.create(section=self.section, question=QUESTION, choices=[
                                           "John", "Jane", "Jack"], scores=[1, 2, 3])
        self.assertNotEqual(question.question, QUESTION_2)
        self.assertNotEqual(question.choices, ["Red", "Blue", "Green"])
        self.assertNotEqual(question.scores, [3, 2, 1])

    def testEditQuestion(self):
        question = Question.objects.create(section=self.section, question=QUESTION, choices=[
                                           "John", "Jane", "Jack"], scores=[1, 2, 3])
        question.question = QUESTION_2
        question.choices = ["Red", "Blue", "Green"]
        question.scores = [3, 2, 1]
        question.save()
        self.assertEqual(question.question, QUESTION_2)
        self.assertEqual(question.choices, ["Red", "Blue", "Green"])
        self.assertEqual(question.scores, [3, 2, 1])

    def testEditQuestionNegative(self):
        question = Question.objects.create(section=self.section, question=QUESTION, choices=[
                                           "John", "Jane", "Jack"], scores=[1, 2, 3])
        question.question = QUESTION_2
        question.choices = ["Red", "Blue", "Green"]
        question.scores = [3, 2, 1]
        question.save()
        self.assertNotEqual(question.question, QUESTION)
        self.assertNotEqual(question.choices, ["John", "Jane", "Jack"])
        self.assertNotEqual(question.scores, [1, 2, 3])

    def testDeleteQuestion(self):
        question = Question.objects.create(section=self.section, question=QUESTION, choices=[
                                           "John", "Jane", "Jack"], scores=[1, 2, 3])
        question.delete()
        self.assertEqual(Question.objects.count(), 0)

    def testDeleteQuestionNegative(self):
        question = Question.objects.create(section=self.section, question=QUESTION, choices=[
                                           "John", "Jane", "Jack"], scores=[1, 2, 3])
        question.delete()
        self.assertNotEqual(Question.objects.count(), 1)

    def testQuestionString(self):
        question = Question.objects.create(section=self.section, question=QUESTION, choices=[
                                           "John", "Jane", "Jack"], scores=[1, 2, 3])
        self.assertEqual(str(question), QUESTION)

    def testQuestionStringNegative(self):
        question = Question.objects.create(section=self.section, question=QUESTION, choices=[
                                           "John", "Jane", "Jack"], scores=[1, 2, 3])
        self.assertNotEqual(str(question), QUESTION_2)

    def testQuestionLabel(self):
        field_label = Question._meta.get_field("question").verbose_name
        self.assertEqual(field_label, "question")

    def testQuestionLabelNegative(self):
        field_label = Question._meta.get_field("question").verbose_name
        self.assertNotEqual(field_label, "not question")

    def testChoicesLabel(self):
        field_label = Question._meta.get_field("choices").verbose_name
        self.assertEqual(field_label, "choices")

    def testChoicesLabelNegative(self):
        field_label = Question._meta.get_field("choices").verbose_name
        self.assertNotEqual(field_label, "not choices")

    def testScoresLabel(self):
        field_label = Question._meta.get_field("scores").verbose_name
        self.assertEqual(field_label, "scores")

    def testScoresLabelNegative(self):
        field_label = Question._meta.get_field("scores").verbose_name
        self.assertNotEqual(field_label, "not scores")


class QuestionApiTest(AuthTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.APPLICANT_BASE_ENDPOINT = "/api/question"
        cls.JSON_CONTENT_TYPE = "application/json"
        cls.controller = QuestionController()
        cls.payload = {
            "question": QUESTION,
            "choices": ["John", "Jane", "Jack"],
            "scores": [1, 2, 3]
        }
        cls.payload_2 = {
            "question": "What is your grade?",
            "choices": ["SMA", "SMP", "SD"],
            "scores": [3, 2, 1]
        }
        cls.test_section = Section.objects.create(
            name="Test Section",
            minimum_score=10,
            create_date=DATETIME,
            update_date=DATETIME
        )
        cls.test_question = Question.objects.create(
            section=cls.test_section, **cls.payload
        )

    def testCreateQuestion(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT + f"/section/{self.test_section.id}",
            data=self.payload_2,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 201)

    def testCreateQuestionNegative(self):
        response = self.client.post(
            self.APPLICANT_BASE_ENDPOINT + f"/section/{self.test_section.id}",
            data=self.payload,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 409)

    def testGetQuestion(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + "/" + str(self.test_question.id),
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testGetQuestionNegative(self):
        response = self.client.get(
            self.APPLICANT_BASE_ENDPOINT + "/" + "10",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def testEditQuestion(self):
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT + "/" + str(self.test_question.id),
            data=self.payload_2,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def testEditQuestionNegative(self):
        response = self.client.put(
            self.APPLICANT_BASE_ENDPOINT + "/" + "10",
            data=self.payload,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def testDeleteQuestion(self):
        response = self.client.delete(
            self.APPLICANT_BASE_ENDPOINT + "/" + str(self.test_question.id),
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 204)

    def testDeleteQuestionNegative(self):
        response = self.client.delete(
            self.APPLICANT_BASE_ENDPOINT + "/" + "10",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)