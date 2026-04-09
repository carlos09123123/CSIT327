from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Foster, FosterApplication, FosterAssignment, FosterCheckIn
from .forms import FosterForm, FosterApplicationForm
from apps.animals.models import Pet

User = get_user_model()

class FosterModelTest(TestCase):
    def test_foster_str(self):
        foster = Foster.objects.create(first_name='John', last_name='Doe', email='john@example.com', phone='1234567890', address='123 Main St')
        self.assertEqual(str(foster), 'John Doe')

class FosterApplicationModelTest(TestCase):
    def setUp(self):
        self.foster = Foster.objects.create(first_name='Jane', last_name='Smith', email='jane@example.com', phone='0987654321', address='456 Elm St')
        self.staff = User.objects.create_user(username='staff', password='pass')

    def test_application_str(self):
        application = FosterApplication.objects.create(foster=self.foster, staff=self.staff)
        self.assertEqual(str(application), 'Foster Application by Jane Smith')

class FosterAssignmentModelTest(TestCase):
    def setUp(self):
        self.foster = Foster.objects.create(first_name='Bob', last_name='Wilson', email='bob@example.com', phone='1112223333', address='789 Oak St')
        self.pet = Pet.objects.create(name='Fluffy', species='Dog', breed='Golden Retriever', age=2, status='Available')
        self.staff = User.objects.create_user(username='staff2', password='pass')

    def test_assignment_str(self):
        assignment = FosterAssignment.objects.create(foster=self.foster, pet=self.pet, staff=self.staff, start_date='2023-01-01')
        self.assertEqual(str(assignment), 'Fluffy fostered by Bob Wilson')

    def test_is_active(self):
        assignment = FosterAssignment.objects.create(foster=self.foster, pet=self.pet, staff=self.staff, start_date='2023-01-01', status='Active')
        self.assertTrue(assignment.is_active)

class FosterCheckInModelTest(TestCase):
    def setUp(self):
        self.foster = Foster.objects.create(first_name='Alice', last_name='Brown', email='alice@example.com', phone='4445556666', address='101 Pine St')
        self.pet = Pet.objects.create(name='Whiskers', species='Cat', breed='Siamese', age=1, status='Available')
        self.staff = User.objects.create_user(username='staff3', password='pass')
        self.assignment = FosterAssignment.objects.create(foster=self.foster, pet=self.pet, staff=self.staff, start_date='2023-01-01')

    def test_checkin_str(self):
        checkin = FosterCheckIn.objects.create(assignment=self.assignment, staff=self.staff, checkin_date='2023-01-15', pet_condition='Good')
        self.assertEqual(str(checkin), 'Check-in for Whiskers on 2023-01-15')

class FosterFormTest(TestCase):
    def test_foster_form_valid(self):
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'address': 'Test Address',
            'occupation': '',
            'has_other_pets': False,
            'has_children': False,
            'experience_years': 0,
            'preferred_species': '',
            'max_pets': 1,
            'notes': '',
        }
        form = FosterForm(data=form_data)
        self.assertTrue(form.is_valid())

class FosterApplicationFormTest(TestCase):
    def setUp(self):
        self.foster = Foster.objects.create(first_name='Form', last_name='Test', email='form@example.com', phone='1234567890', address='Form Address')

    def test_application_form_valid(self):
        form_data = {
            'foster': self.foster.pk,
            'status': 'Pending',
            'notes': 'Test notes',
        }
        form = FosterApplicationForm(data=form_data)
        self.assertTrue(form.is_valid())

class FosterViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.foster = Foster.objects.create(first_name='View', last_name='Test', email='view@example.com', phone='1234567890', address='View Address')
        self.client.login(username='testuser', password='pass')

    def test_foster_list_view(self):
        response = self.client.get(reverse('foster_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View Test')

    def test_foster_add_view(self):
        response = self.client.post(reverse('foster_add'), {
            'first_name': 'New',
            'last_name': 'Foster',
            'email': 'new@example.com',
            'phone': '1234567890',
            'address': 'New Address',
            'occupation': '',
            'has_other_pets': False,
            'has_children': False,
            'experience_years': 0,
            'preferred_species': '',
            'max_pets': 1,
            'notes': '',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Foster.objects.filter(email='new@example.com').exists())

    def test_application_delete_view(self):
        application = FosterApplication.objects.create(foster=self.foster, staff=self.user)
        response = self.client.post(reverse('application_delete', kwargs={'pk': application.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FosterApplication.objects.filter(pk=application.pk).exists())
