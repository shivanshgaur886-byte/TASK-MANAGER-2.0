from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class PasswordResetTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='tester', email='tester@example.com', password='strong-pass')

    def test_password_reset_pages_load(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_email_sent(self):
        response = self.client.post(reverse('password_reset'), {'email': 'tester@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))

