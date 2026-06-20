# users/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class RegistrationTest(TestCase):
    def test_registration_page_status(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_registration_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
            'email': 'new@example.com'
        })
        self.assertRedirects(response, reverse('book_list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_passwords_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'password1': 'ComplexPass123',
            'password2': 'DifferentPass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser2').exists())
        self.assertFormError(response.context['form'], 'password2', 'The two password fields didn’t match.')

class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_page_status(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertRedirects(response, reverse('book_list'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='pass')
        self.client.login(username='profileuser', password='pass')

    def test_profile_page_authenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, 'profileuser')

    def test_profile_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)