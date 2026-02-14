from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
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
        self.client.credentials()
        data = {
            'tag': self.tag.id,
            'data': '90'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MetricRecord.objects.count(), 0)

    def test_create_record_without_data(self):
        """Тест создания записи без данных"""
        missing_data = {
            'tag': self.tag.id
        }
        response = self.client.post(self.url, missing_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MetricRecord.objects.count(), 0)

    def test_create_record_invalid_tag(self):
        """Тест создания записи с несуществующим tag"""
        wrong_id = {
            'tag': 999,
            'data': '90'
        }
        response = self.client.post(self.url, wrong_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MetricRecord.objects.count(), 0)

    def test_create_record_invalid_metric(self):
        """Тест создания записи у несуществующей метрики"""
        invalid_url = '/api/metrics/999/records/'
        wrong_metric = {
            'tag': self.tag.id,
            'data': '90',
        }
        response = self.client.post(invalid_url, wrong_metric, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(MetricRecord.objects.count(), 0)

    def test_create_record_invalid_token(self):
        """Тест создания записи с недействительным токеном авторизации"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer invalid_token_12345'
        )
        data = {
            'tag': self.tag.id,
            'data': '90'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(MetricRecord.objects.count(), 0)

    def test_create_record_success(self):
        """Тест успешного создания записи"""
        data = {
            'tag': self.tag.id,
            'data': '90',
            'metric': self.metric.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MetricRecord.objects.count(), 1)
