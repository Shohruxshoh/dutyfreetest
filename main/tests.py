from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import FAQ


class FAQListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some FAQ objects for testing
        for i in range(15):  # Create 15 FAQs to test pagination
            FAQ.objects.create(question=f'Question {i}', answer=f'Answer {i}')

    def test_faq_list_pagination(self):
        url = reverse('faq-list')  # Assuming your FAQListView is mapped to 'faq-list'

        # Test with page_size=5
        response = self.client.get(url, {'page_size': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # Should return 5 items

        # Test with page_size=10
        response = self.client.get(url, {'page_size': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Should return 10 items

        # Test with page_size exceeding the number of available items
        response = self.client.get(url, {'page_size': 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 15)  # Should return all 15 items

    def test_faq_list_default_pagination(self):
        url = reverse('faq-list')

        # Test with default pagination
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the default page size is applied (depends on the default set in the pagination class)
        self.assertTrue(len(response.data) > 0)
