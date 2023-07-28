from django.test import TestCase
from .models import User
from django.test import Client
from decouple import config
from ninja_jwt.tokens import RefreshToken

FIRST_ADMIN = "first admin"
NOT_ADMIN = "not admin"
FIRST_SU = "first_su"
NOT_SU = "not_su"

class AdminAccountTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create(first_name=FIRST_ADMIN, email=FIRST_ADMIN, password=config('test_admin_password'))

    def testCreateAdmin(self):
        self.assertEqual(self.admin.first_name+self.admin.last_name, FIRST_ADMIN)

    def testObjectStrings(self):
        self.assertEqual(str(self.admin), FIRST_ADMIN)
        self.assertEqual(str(self.admin.admin), FIRST_ADMIN)

    def testFirstNameField(self):
        first_name = self.admin.first_name
        self.assertEqual(first_name, FIRST_ADMIN)
        
    def testFirstNameFieldNegative(self):
        first_name = self.admin.first_name
        self.assertNotEqual(first_name, NOT_ADMIN)

    def testFirstNameLabel(self):
        field_label = self.admin._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def testFirstNameLabelNegative(self):
        field_label = self.admin._meta.get_field('first_name').verbose_name
        self.assertNotEqual(field_label, 'not first_name')

    def testLastNameLabel(self):
        field_label = self.admin._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def testLastNameLabelNegative(self):
        field_label = self.admin._meta.get_field('last_name').verbose_name
        self.assertNotEqual(field_label, 'not last_name')

    def testEmailField(self):
        email = self.admin.email
        self.assertEqual(email, FIRST_ADMIN)

    def testEmailFieldNegative(self):
        email = self.admin.email
        self.assertNotEqual(email, 'NOT_ADMIN')

    def testEmailLabel(self):
        field_label = self.admin._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def testEmailLabelNegative(self):
        field_label = self.admin._meta.get_field('email').verbose_name
        self.assertNotEqual(field_label, NOT_ADMIN)

    def testPasswordField(self):
        password = self.admin.password
        self.assertEqual(password, config('test_admin_password'))

    def testPasswordFieldNegative(self):
        password = self.admin.password
        self.assertNotEqual(password, 'not admin')
        
    def testBranchLabel(self):
        field_label = self.admin._meta.get_field('branch').verbose_name
        self.assertEqual(field_label, 'branch')

    def testBranchLabelNegative(self):
        field_label = self.admin._meta.get_field('branch').verbose_name
        self.assertNotEqual(field_label, 'not branch')

class TokenAuthenticationTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(email=FIRST_ADMIN, password=config('test_admin_password'))

        self.refresh = RefreshToken.for_user(user=self.admin)
        self.pair_token = {
            'refresh': str(self.refresh),
            'access': str(self.refresh.access_token)
        }
        
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.pair_token['access'],
        }
    
    def testRequireToken(self):
        response = self.client.get('/api/auth/test')
        self.assertEqual(response.status_code, 401)
    
    def testTokenProvided(self):
        response = self.client.get('/api/auth/test', **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})


    def testLoginShouldReturnToken(self):
        self.assertTrue(self.client.login(email=FIRST_ADMIN, password=config('test_admin_password')))

class SuperUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(email=FIRST_SU, password=config('test_superuser_password'))

        self.refresh = RefreshToken.for_user(user=self.superuser)
        self.pair_token = {
            'refresh': str(self.refresh),
            'access': str(self.refresh.access_token)
        }
        
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.pair_token['access'],
        }

    def testStaffAndSuperuserField(self):
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

    def testObjectStrings(self):
        self.assertEqual(str(self.superuser), FIRST_SU)