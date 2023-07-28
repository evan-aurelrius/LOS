from decouple import config
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from ninja_jwt.tokens import RefreshToken

from account.models import User
from applicant.tests import AuthTestCase
from loanproduct.admin import SoftDeleteModelAdmin
from loanproduct.api import LoanProductController
from loanproduct.models import LoanProduct, LoanProductSection
from section.models import Section


class LoanProductModelTest(TestCase):

    def setUp(self):
        self.DATETIME = "2010-10-10 10:10:10"
        self.loan_product = LoanProduct.objects.create(
            name="Asuransi Rumah",
            description="Houser",
            category="Default",
            create_date=self.DATETIME,
            update_date=self.DATETIME
        )

    def test_name_field(self):
        expected = "Asuransi Rumah"
        actual = self.loan_product.name
        self.assertEqual(expected, actual)

    def test_description_field(self):
        expected = "Houser"
        actual = self.loan_product.description
        self.assertEqual(expected, actual)

    def test_category_field(self):
        expected = "Default"
        actual = self.loan_product.category
        self.assertEqual(expected, actual)

    def test_create_date_field(self):
        expected = self.DATETIME
        actual = self.loan_product.create_date
        self.assertEqual(expected, actual)

    def test_update_date_field(self):
        expected = self.DATETIME
        actual = self.loan_product.update_date
        self.assertEqual(expected, actual)

    def test_str_method(self):
        self.assertEqual(str(self.loan_product), self.loan_product.name)


class LoanProductSectionModelTest(TestCase):

    def setUp(self):
        self.DATETIME = "2010-10-10 10:10:10"
        self.loan_product = LoanProduct.objects.create(
            name="Asuransi Kejiwaan",
            description="Healio",
            category="Default",
            create_date=self.DATETIME,
            update_date=self.DATETIME
        )
        self.section = Section.objects.create(
            name="Kebhinekaan",
            minimum_score=10,
            create_date=self.DATETIME,
            update_date=self.DATETIME
        )
        self.loan_product_section = LoanProductSection.objects.create(
            loan_product=self.loan_product,
            section=self.section,
            order=1,
        )

    def test_str_method(self):
        self.assertEqual(str(self.loan_product_section), f'{self.loan_product} - {self.section}')


class LoanProductControllerTestCase(AuthTestCase):
    @classmethod
    def setUpClass(cls):
        super(LoanProductControllerTestCase, cls).setUpClass()
        cls.LOAN_PRODUCT_API_ENDPOINT = "/api/loanproduct"
        cls.JSON_CONTENT_TYPE = "application/json"
        cls.DATETIME = "2023-04-14 00:00:00"
        cls.controller = LoanProductController()
        cls.client = Client(cls.controller)

        cls.product1 = LoanProduct.objects.create(
            name="Asuransi Mobil",
            description="2019 Honda Mobilio",
            category="Default Product",
            create_date=cls.DATETIME,
            update_date=cls.DATETIME
        )

        cls.product2 = LoanProduct.objects.create(
            name="Asuransi Motor",
            description="2019 Honda Motorio",
            category="Default Product",
            create_date=cls.DATETIME,
            update_date=cls.DATETIME
        )

        cls.section1 = Section.objects.create(
            name="Pendidikan",
            minimum_score=10,
            create_date=cls.DATETIME,
            update_date=cls.DATETIME
        )

        cls.section2 = Section.objects.create(
            name="Kejiwaan",
            minimum_score=10,
            create_date=cls.DATETIME,
            update_date=cls.DATETIME
        )

        cls.payload_create_1 = {
            "name": "Kos",
            "description": "Peminjaman untuk kos",
            "category": "Secured"
        }

        cls.payload_create_2 = {
            "name": "Asuransi Pendidikan",
            "description": "Scholaris",
            "category": "Secured"
        }

        cls.payload_create_3 = {
            "name": "Del",
            "description": "Del",
            "category": "Secured"
        }

        cls.payload_update = {
            "name": "Asuransi Kesehatan",
            "description": "Krudensial",
            "category": "Secured"
        }

    def test_create_loan_product(self):
        response = self.client.post(
            self.LOAN_PRODUCT_API_ENDPOINT,
            self.payload_create_1,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("loan_product_id", response.json())
        loan_product_id = response.json()['loan_product_id']
        loan_product = LoanProduct.objects.get(id=loan_product_id)
        self.assertEqual(loan_product.name, "Kos")
        self.assertEqual(loan_product.description, "Peminjaman untuk kos")
        self.assertEqual(loan_product.category, "Secured")

    def test_read_loan_product_list(self):
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + "/list",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(len(response.json()["items"]), 2)

        product1, product2 = response.json()["items"]
        self.assertEqual(product1["name"], self.product1.name)
        self.assertEqual(product2["name"], self.product2.name)

    def test_read_loan_product_list_pagination(self):
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + "/list?limit=1&offset=0",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(len(response.json()["items"]), 1)

        product1 = response.json()["items"][0]
        self.assertEqual(product1["name"], self.product1.name)

    def test_read_loan_product_list_filter(self):
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + f"/list?product_id={self.product2.id}&product_name=Asuransi Motor&description=2019 Honda Motorio&category=Default Product",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["items"]), 1)

        product1 = response.json()["items"][0]
        self.assertEqual(product1["name"], self.product2.name)

    def test_read_loan_product_list_filter_by_date(self):
        product_create_date = "2023-04-14"
        product_update_date = "2023-04-14"
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + f"/list?create_date_start={product_create_date}&create_date_end={product_create_date}&update_date_start={product_update_date}&update_date_end={product_update_date}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers

        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(len(response.json()["items"]), 2)

    def test_read_loan_product_list_filter_by_date_invalid_format(self):
        product_create_date = "14-04-2023"
        product_update_date = "14-04-2023"
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + f"/list?create_date_start={product_create_date}&create_date_end={product_create_date}&update_date_start={product_update_date}&update_date_end={product_update_date}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)

    def test_read_loan_product_detail(self):
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + f"/{self.product2.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        loan_product_id = response.json()['id']
        loan_product = LoanProduct.objects.get(id=loan_product_id)
        self.assertEqual(loan_product.name, self.product2.name)
        self.assertEqual(loan_product.description, self.product2.description)
        self.assertEqual(loan_product.category, self.product2.category)

    def test_read_loan_product_detail_not_found(self):
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + "/999",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_loan_product(self):
        response = self.client.post(
            self.LOAN_PRODUCT_API_ENDPOINT,
            self.payload_create_2,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        loan_product_id = response.json()['loan_product_id']
        old_loan_product = LoanProduct.objects.get(id=loan_product_id)
        response = self.client.put(
            self.LOAN_PRODUCT_API_ENDPOINT + "/" + str(old_loan_product.id),
            self.payload_update,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        new_loan_product = LoanProduct.objects.get(id=loan_product_id)
        self.assertNotEqual(old_loan_product.name, new_loan_product.name)
        self.assertEqual(new_loan_product.name, "Asuransi Kesehatan")

    def test_update_loan_product_not_found(self):
        response = self.client.put(
            self.LOAN_PRODUCT_API_ENDPOINT + "/999",
            self.payload_update,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_loan_product(self):
        response = self.client.post(
            self.LOAN_PRODUCT_API_ENDPOINT,
            self.payload_create_3,
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        old_count = LoanProduct.objects.count()
        loan_product_id = response.json()['loan_product_id']
        response = self.client.delete(
            self.LOAN_PRODUCT_API_ENDPOINT + "/" + str(loan_product_id),
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        new_count = LoanProduct.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(old_count - 1, new_count)

    def test_delete_loan_product_not_found(self):
        response = self.client.delete(
            self.LOAN_PRODUCT_API_ENDPOINT + "/999",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_loan_product_section(self):
        response = self.client.post(
            self.LOAN_PRODUCT_API_ENDPOINT + f"/sections/{self.product1.id}",
            [self.section2.id, self.section1.id],
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        loan_product_id = response.json()['loan_product_id']
        loan_product = LoanProduct.objects.get(id=loan_product_id)
        self.assertEqual([self.section2.id, self.section1.id],
                         list(loan_product.sections.order_by('loanproductsection').values_list('id', flat=True)))

    def test_update_loan_product_section_not_found(self):
        response = self.client.post(
            self.LOAN_PRODUCT_API_ENDPOINT + "/sections/999",
            [self.section2.id, self.section1.id],
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_loan_product_section_doesnt_match(self):
        response = self.client.post(
            self.LOAN_PRODUCT_API_ENDPOINT + f"/sections/{self.product1.id}",
            [3, 4],
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 400)

    def test_get_loan_product_section(self):
        self.client.post(
            self.LOAN_PRODUCT_API_ENDPOINT + f"/sections/{self.product1.id}",
            [self.section1.id, self.section2.id],
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + f"/sections/{self.product1.id}",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        section1 = response.json()[0]
        section2 = response.json()[1]
        self.assertEqual(section1["id"], str(self.section1.id))
        self.assertEqual(section2["id"], str(self.section2.id))

    def test_get_loan_product_section_not_found(self):
        response = self.client.get(
            self.LOAN_PRODUCT_API_ENDPOINT + "/sections/999",
            content_type=self.JSON_CONTENT_TYPE,
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 404)


class SoftDeleteModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(first_name='first', last_name='last', password='password',
                                             email='test@email.com')
        self.loan_product = LoanProduct.objects.create(name='Test Product')
        self.soft_deleted_product = LoanProduct.objects.create(name='Soft Deleted Product', is_deleted=True)
        self.section = Section.objects.create(name="Test Section")
        self.loan_product_section = LoanProductSection.objects.create(
            loan_product=self.loan_product,
            section=self.section,
            order=1,
        )

    def test_soft_delete(self):
        self.assertFalse(self.loan_product.is_deleted)
        self.assertIsNone(self.loan_product.deleted_at)
        self.assertIsNone(self.loan_product.deleted_by)

        self.loan_product.soft_delete(user=self.user)

        self.assertTrue(self.loan_product.is_deleted)
        self.assertIsNotNone(self.loan_product.deleted_at)
        self.assertEqual(self.loan_product.deleted_by, self.user)

    def test_soft_delete_with_related_objects(self):
        self.loan_product.soft_delete(user=self.user)

        with self.assertRaises(LoanProductSection.DoesNotExist):
            LoanProductSection.objects.get(loan_product=self.loan_product)

    def test_delete(self):
        self.assertFalse(self.loan_product.is_deleted)
        self.assertIsNone(self.loan_product.deleted_at)
        self.assertIsNone(self.loan_product.deleted_by)

        self.loan_product.delete(user=self.user)

        self.assertTrue(self.loan_product.is_deleted)
        self.assertIsNotNone(self.loan_product.deleted_at)
        self.assertEqual(self.loan_product.deleted_by, self.user)

    def test_restore(self):
        self.soft_deleted_product.restore()

        self.assertFalse(self.soft_deleted_product.is_deleted)
        self.assertIsNone(self.soft_deleted_product.deleted_at)
        self.assertIsNone(self.soft_deleted_product.deleted_by)


class SoftDeleteModelAdminTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(first_name='first', last_name='last', password='password',
                                             email='test@email.com')
        self.permission = Permission.objects.get(codename='view_loanproduct')
        self.user.user_permissions.add(self.permission)
        self.loan_product = LoanProduct.objects.create(name='Test Product 2')
        self.ADMIN_LOANPRODUCT = 'admin:loanproduct_loanproduct_changelist'

    def test_soft_delete_selected(self):
        request = self.factory.post(reverse(self.ADMIN_LOANPRODUCT))
        request.user = self.user
        queryset = LoanProduct.objects.all()
        model_admin = SoftDeleteModelAdmin(LoanProduct, admin.site)
        model_admin.soft_delete_selected(request, queryset)
        self.loan_product.refresh_from_db()
        self.assertEqual(self.loan_product.is_deleted, True)

    def test_restore_selected(self):
        request = self.factory.post(reverse(self.ADMIN_LOANPRODUCT))
        request.user = self.user
        self.loan_product.soft_delete()
        queryset = LoanProduct.all_objects.all()
        model_admin = SoftDeleteModelAdmin(LoanProduct, admin.site)
        model_admin.restore_selected(request, queryset)
        self.loan_product.refresh_from_db()
        self.assertEqual(self.loan_product.is_deleted, False)

    def test_get_queryset(self):
        request = self.factory.get(reverse(self.ADMIN_LOANPRODUCT))
        request.user = self.user
        model_admin = SoftDeleteModelAdmin(LoanProduct, admin.site)
        qs = model_admin.get_queryset(request)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().name, 'Test Product 2')
