from decouple import config
from django.test import TestCase, Client
from ninja_jwt.tokens import RefreshToken

from account.models import User
from applicant.tests import AuthTestCase
from question.models import Question
from section.api import SectionController
from section.models import Section


class SectionModelTestCase(TestCase):
    def setUp(self):
        self.DATETIME = "2010-10-10 10:10:10"
        self.section = Section.objects.create(
            name="Ekonomi",
            minimum_score=10,
            create_date=self.DATETIME,
            update_date=self.DATETIME
        )

    def test_name_field(self):
        expected = "Ekonomi"
        actual = self.section.name
        self.assertEqual(expected, actual)

    def test_minimum_score_field(self):
        expected = 10
        actual = self.section.minimum_score
        self.assertEqual(expected, actual)

    def test_create_date_field(self):
        expected = self.DATETIME
        actual = self.section.create_date
        self.assertEqual(expected, actual)

    def test_update_date_field(self):
        expected = self.DATETIME
        actual = self.section.update_date
        self.assertEqual(expected, actual)

    def test_str_method(self):
        self.assertEqual(str(self.section), self.section.name)


class SectionControllerTestCase(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super(SectionControllerTestCase, cls).setUpClass()
        cls.SECTION_API_ENDPOINT = "/api/section"
        cls.JSON_CONTENT_TYPE = "application/json"
        cls.controller = SectionController()
        cls.client = Client(cls.controller)

        cls.section1 = Section.objects.create(
            name="Section 1",
            minimum_score=10,
            create_date="2023-04-14 00:00:00",
            update_date="2023-04-14 00:00:00"
        )

        cls.section2 = Section.objects.create(
            name="Section 2",
            minimum_score=20,
            create_date="2023-04-15 00:00:00",
            update_date="2023-04-15 00:00:00"
        )

        cls.question1 = Question.objects.create(
            section=cls.section1,
            question="Question 1",
            choices=["A", "B", "C"],
            scores=[1, 2, 3]
        )

        cls.question2 = Question.objects.create(
            section=cls.section1,
            question="Question 2",
            choices=["A", "B", "C"],
            scores=[1, 2, 3]
        )

        cls.payload_create = {
            "name": "Section Create",
            "minimum_score": 10
        }

        cls.payload_update = {
            "name": "Section Update",
            "minimum_score": 20
        }

        cls.payload_create_question = {
            "question": "Question Create",
            "choices": ["A", "B", "C"],
            "scores": [1, 2, 3]
        }

    def test_create_section(self):
        response = self.client.post(
            self.SECTION_API_ENDPOINT,
            self.payload_create,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        section_id = response.json()['section_id']
        section = Section.objects.get(id=section_id)
        self.assertEqual(section.name, self.payload_create.get("name"))
        self.assertEqual(section.minimum_score, self.payload_create.get("minimum_score"))

    def test_read_section_list(self):
        response = self.client.get(
            self.SECTION_API_ENDPOINT + "/list",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(len(response.json()["items"]), 2)

    def test_read_section_list_filter(self):
        response = self.client.get(
            self.SECTION_API_ENDPOINT + f"/list?section_id={self.section1.id}&section_name=Section 1&section_minimum_score=10",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["items"]), 1)

        section = response.json()["items"][0]
        self.assertEqual(section["id"], str(self.section1.id))

    def test_read_section_list_filter_by_date(self):
        date = "2023-04-15"
        response = self.client.get(
            self.SECTION_API_ENDPOINT + f"/list?create_date_start={date}&create_date_end={date}&update_date_start={date}&update_date_end={date}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["items"]), 1)

        section = response.json()["items"][0]
        self.assertEqual(section["id"], str(self.section2.id))

    def test_read_section_list_filter_by_date_invalid_format(self):
        date = "15-04-2023"
        response = self.client.get(
            self.SECTION_API_ENDPOINT + f"/list?create_date_start={date}&create_date_end={date}&update_date_start={date}&update_date_end={date}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)

    def test_read_section_detail(self):
        response = self.client.get(
            self.SECTION_API_ENDPOINT + f"/{self.section2.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        section_id = response.json()['id']
        section_name = response.json()['name']
        section_minimum_score = response.json()['minimum_score']
        self.assertEqual(section_id, str(self.section2.id))
        self.assertEqual(section_name, self.section2.name)
        self.assertEqual(section_minimum_score, self.section2.minimum_score)

    def test_read_section_detail_not_found(self):
        response = self.client.get(
            self.SECTION_API_ENDPOINT + "/999",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_section(self):
        response = self.client.post(
            self.SECTION_API_ENDPOINT,
            self.payload_create,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        section_id = response.json()['section_id']
        old_section = Section.objects.get(id=section_id)
        response = self.client.put(
            self.SECTION_API_ENDPOINT + "/" + str(section_id),
            self.payload_update,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        new_section = Section.objects.get(id=section_id)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(old_section.name, new_section.name)
        self.assertEqual(new_section.name, self.payload_update.get("name"))

    def test_update_section_not_found(self):
        response = self.client.put(
            self.SECTION_API_ENDPOINT + "/999",
            self.payload_update,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_section(self):
        response = self.client.post(
            self.SECTION_API_ENDPOINT,
            self.payload_create,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        old_count = Section.objects.count()
        section_id = response.json()['section_id']
        response = self.client.delete(
            self.SECTION_API_ENDPOINT + "/" + str(section_id),
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        new_count = Section.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(old_count - 1, new_count)

    def test_delete_section_not_found(self):
        response = self.client.delete(
            self.SECTION_API_ENDPOINT + "/999",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_create_section_question(self):
        response = self.client.post(
            self.SECTION_API_ENDPOINT + f"/questions/{self.section1.id}",
            self.payload_create_question,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        question_id = response.json()['question_id']
        question = Question.objects.get(id=question_id)
        self.assertEqual(question.section_id, self.section1.id)
        self.assertEqual(question.question, self.payload_create_question.get("question"))
        self.assertEqual(question.choices, self.payload_create_question.get("choices"))
        self.assertEqual(question.scores, self.payload_create_question.get("scores"))

    def test_create_section_question_not_found(self):
        response = self.client.post(
            self.SECTION_API_ENDPOINT + "/questions/999",
            self.payload_create_question,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_get_section_question_list(self):
        response = self.client.get(
            self.SECTION_API_ENDPOINT + f"/questions/{self.section1.id}/list",
            self.payload_create_question,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        question1 = response.json()[0]
        question2 = response.json()[1]
        self.assertEqual(question1["id"], self.question1.id)
        self.assertEqual(question2["id"], self.question2.id)

    def test_get_section_question_list_not_found(self):
        response = self.client.get(
            self.SECTION_API_ENDPOINT + "/questions/999/list",
            self.payload_create_question,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_section_question_order(self):
        response = self.client.put(
            self.SECTION_API_ENDPOINT + f"/questions/{self.section1.id}/order",
            [self.question2.id, self.question1.id],
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.section1.get_question_order()), [self.question2.id, self.question1.id])

    def test_update_section_question_order_not_found(self):
        response = self.client.put(
            self.SECTION_API_ENDPOINT + "/questions/999/order",
            [2, 1],
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_section_question_order_doesnt_match(self):
        response = self.client.put(
            self.SECTION_API_ENDPOINT + f"/questions/{self.section1.id}/order",
            [998, 999],
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)