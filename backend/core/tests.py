from django.urls import reverse
from rest_framework.test import APITestCase


class HealthEndpointTests(APITestCase):
	def test_health_endpoint_is_public_and_minimal(self):
		response = self.client.get(reverse('health'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, {'status': 'ok'})
