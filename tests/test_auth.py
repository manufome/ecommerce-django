from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/v1/auth/register/'
        self.login_url = '/api/v1/auth/login/'
        self.user_url = '/api/v1/auth/user/'
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'Testpassword123!',
            'confirm_password': 'Testpassword123!'
        }

    def test_register(self):
        """
        Ensure we can create a new user object.
        """
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_login(self):
        """
        Ensure we can login and get tokens.
        """
        # First register
        self.client.post(self.register_url, self.user_data)
        
        # Then login
        login_data = {
            'username': 'testuser',
            'password': 'Testpassword123!'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        return response.data['access']

    def test_protected_route(self):
        """
        Ensure we can access protected route with token.
        """
        # Register and Login to get token
        access_token = self.test_login()
        
        # Try to access protected route
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
