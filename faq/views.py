from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache
from django.http import JsonResponse
from .models import FAQ
from .serializers import FAQSerializer


class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get(self, request, *args, **kwargs):
        lang = request.GET.get('lang', 'en')
        cache_key = f'faq_list_{lang}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        faqs = self.get_queryset()
        data = [
            {
                "id": faq.id,
                "question": faq.get_translated_question(lang),
                "answer": faq.answer
            }
            for faq in faqs
        ]
        cache.set(cache_key, data, timeout=3600)
        return Response(data)


def index(request):
    return JsonResponse({"message": "Welcome to the FAQ API!"})
