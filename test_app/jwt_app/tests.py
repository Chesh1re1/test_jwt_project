from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .views import MetricViewSet
from .models import Metric, Tag, MetricRecord


class MetricRecordCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user',
            password='testpwd123',
            email=''
        )
        token_response = self.client.post(
            '/api/token/',{
                'username': 'test_user',
                'password': 'testpwd123'
            }, format='json'
        )
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.metric = Metric.objects.create(name='revenue')
        self.tag = Tag.objects.create(name='Android')
        self.url = f'/api/metrics/{self.metric.id}/records/'

    def tearDown(self):
        self.client.credentials()

    def test_create_record_unauthorized(self):
        """Тест создания записи без авторизации"""
        # Убираем токен
        self.client.credentials()

        data = {
            'tag_ids': [self.tag.id],
            'data': '90'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MetricRecord.objects.count(), 0)
