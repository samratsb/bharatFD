import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from faq.models import FAQ


@pytest.mark.django_db
def test_faq_api():
    client = APIClient()

    faq = FAQ.objects.create(
        question="hello how are you?",
        answer="I am fine, thank you"
    )

    url = reverse('faq-list')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["question"] == faq.question
