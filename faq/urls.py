from django.urls import path
from .views import index, FAQListView

urlpatterns = [
    path('', index, name='index'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
]
