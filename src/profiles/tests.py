from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from src.profiles.models import FatUser, Social

user_create_data = {
    'username': 'anton',
    'password': 'V97tn7M4rU',
    're_password': 'V97tn7M4rU',
    'email': 'antonenique@example.com'
}


class ProfileRegTests(APITestCase):
    def test_create_user(self):
        self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        user = FatUser.objects.get(email='antonenique@example.com')
        self.assertEqual(user.username, 'anton')
        self.assertEqual(user.email, 'antonenique@example.com')

    def test_create_user_error_pass(self):
        data = user_create_data.copy()
        data['re_password'] = 'V97tn7M4ru'
        request = self.client.post('/api/v1/auth/users/', data, format='json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.data['non_field_errors'][0].title(), 'Два Пароля Не Совпадают.')

    def test_create_user_required(self):
        error_msg = 'Обязательное Поле.'
        request = self.client.post('/api/v1/auth/users/', {}, format='json')
        self.assertEqual(request.data['email'][0].title(), error_msg)
        self.assertEqual(request.data['username'][0].title(), error_msg)
        self.assertEqual(request.data['password'][0].title(), error_msg)
        self.assertEqual(request.data['re_password'][0].title(), error_msg)

    def test_create_user_unique(self):
        self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        request = self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        self.assertEqual(
            request.data['email'][0].title(),
            'Пользователь С Таким Адрес Электронной Почты Уже Существует.'
        )

        self.assertEqual(
            request.data['username'][0].title(),
            'Пользователь С Таким Именем Уже Существует.'
        )


class ProfileAuthTests(APITestCase):
    def setUp(self):
        self.client.post('/api/v1/auth/users/', user_create_data, format='json')
        url = "/api/v1/auth/token/login/"
        user = {
            'email': user_create_data['email'],
            'password': user_create_data['password']
        }
        request = self.client.post(url, user, format='json')
        self.assertEqual(request.status_code, 200)
        self.assertTrue('auth_token' in request.data)

    def test_user_pub_profile(self):
        user = FatUser.objects.get(username='anton')
        url = reverse("user-pub", kwargs={"pk": user.pk})
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertFalse('email' in request.data)

    def test_user_profile(self):
        user = FatUser.objects.get(username='anton')
        url = reverse("user")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertTrue('email' in request.data)


class TestSocial(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        Social.objects.create(title='Social 1')
        Social.objects.create(title='Social 2')

    def test_social_list(self):
        url = reverse("social-list")
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 2)

    def test_social_detail(self):
        social = Social.objects.get(title='Social 1')
        url = reverse("social-detail", kwargs={"pk": social.pk})
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['title'], 'Social 1')
