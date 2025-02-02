import pytest
from django.core.cache import cache
from faq.models import FAQ


@pytest.mark.django_db
def test_get_translated_question():
    faq = FAQ.objects.create(
        question="hello how are you?",
        answer="I am fine, thank you"
    )
    faq.question_hi = "नमस्ते, आप कैसे हैं?"
    faq.question_bn = "হ্যালো কেমন আছেন?"
    faq.save()

    # Test that the original language is returned if no cache
    assert faq.get_translated_question("en") == "hello how are you?"

    # Test that the Hindi translation is fetched correctly
    assert faq.get_translated_question("hi") == "नमस्ते, आप कैसे हैं?"

    # Test that Bengali translation is fetched correctly
    assert faq.get_translated_question("bn") == "হ্যালো কেমন আছেন?"

    # Test that cache is used for faster retrieval
    cached_question = cache.get(f'faq_{faq.id}_question_hi')
    assert cached_question == "नमस्ते, आप कैसे हैं?"


@pytest.mark.django_db
def test_no_translation_in_cache():
    # Clear cache before the test to ensure it is empty
    cache.clear()

    faq = FAQ.objects.create(
        question="hello how are you?",
        answer="I am fine, thank you"
    )

    # Test that the original language is returned if no translation in cache
    assert faq.get_translated_question("en") == "hello how are you?"


@pytest.mark.django_db
def test_fallback_to_original_language():
    faq = FAQ.objects.create(
        question="hello how are you?",
        answer="I am fine, thank you"
    )
    # Test that no translation falls back to the original language
    assert faq.get_translated_question("fr") == "hello how are you?"
    # fr unavailable


@pytest.mark.django_db
def test_cache_update_on_translation_change():
    faq = FAQ.objects.create(
        question="hello how are you?",
        answer="I am fine, thank you"
    )
    faq.question_hi = "नमस्ते, आप कैसे हैं?"
    faq.save()

    # Initially, check the Hindi translation in cache
    cached_question = cache.get(f'faq_{faq.id}_question_hi')
    assert cached_question == "नमस्ते, आप कैसे हैं?"  # This is set in save()

    # Change the translation and save again
    faq.question_hi = "नमस्ते, क्या हाल है?"
    faq.save()

    # Test that the cache is updated after modification
    cached_question = cache.get(f'faq_{faq.id}_question_hi')
    assert cached_question == "नमस्ते, क्या हाल है?"
