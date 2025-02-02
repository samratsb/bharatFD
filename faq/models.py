from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.cache import cache
from googletrans import Translator


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = CKEditor5Field('answer', config_name='default')
    question_hi = models.CharField(max_length=255, blank=True, null=True)
    question_bn = models.CharField(max_length=255, blank=True, null=True)
    answer_hi = CKEditor5Field('answer_hi', config_name='default', blank=True, null=True)
    answer_bn = CKEditor5Field('answer_bn', config_name='default', blank=True, null=True)

    def get_translated_question(self, lang):
        """
        Returns translated question if it exists, else original question.
        """
        # Check if the requested translation exists in the cache first
        cached_question = cache.get(f'faq_{self.id}_question_{lang}')
        if cached_question:
            return cached_question

        # If no cache, fallback to the model fields
        if lang == 'hi' and self.question_hi:
            return self.question_hi
        elif lang == 'bn' and self.question_bn:
            return self.question_bn

        # If no translation exists, return original question and cache it
        cache.set(f'faq_{self.id}_question_{lang}', self.question, timeout=86400)
        return self.question

    def get_translated_answer(self, lang):
        """
        Returns translated answer if it exists, else original answer.
        """
        # Check if the requested translation exists in the cache first
        cached_answer = cache.get(f'faq_{self.id}_answer_{lang}')
        if cached_answer:
            return cached_answer

        # If no cache, fallback to the model fields
        if lang == 'hi' and self.answer_hi:
            return self.answer_hi
        elif lang == 'bn' and self.answer_bn:
            return self.answer_bn

        # If no translation exists, return original answer and cache it
        cache.set(f'faq_{self.id}_answer_{lang}', self.answer, timeout=86400)
        return self.answer

def save(self, *args, **kwargs):
    """
    Save the FAQ instance.
    Translates the question and answer if not yet translated.
    Caches translations for efficiency.
    """
    translator = Translator()

    # Translate question to Hindi if not already translated
    if not self.question_hi:
        try:
            self.question_hi = translator.translate(self.question, dest='hi').text
            cache.set(f'faq_{self.id}_question_hi', self.question_hi, timeout=86400)
        except Exception as e:
            print(f"Error translating question to Hindi: {e}")
            self.question_hi = self.question

    # Translate question to Bengali if not already translated
    if not self.question_bn:
        try:
            self.question_bn = translator.translate(self.question, dest='bn').text
            cache.set(f'faq_{self.id}_question_bn', self.question_bn, timeout=86400)
        except Exception as e:
            print(f"Error translating question to Bengali: {e}")
            self.question_bn = self.question

    # Translate answer to Hindi if not already translated
    if not self.answer_hi and self.answer:
        try:
            self.answer_hi = translator.translate(self.answer, dest='hi').text
            cache.set(f'faq_{self.id}_answer_hi', self.answer_hi, timeout=86400)
        except Exception as e:
            print(f"Error translating answer to Hindi: {e}")
            self.answer_hi = self.answer

    # Translate answer to Bengali if not already translated
    if not self.answer_bn and self.answer:
        try:
            self.answer_bn = translator.translate(self.answer, dest='bn').text
            cache.set(f'faq_{self.id}_answer_bn', self.answer_bn, timeout=86400)
        except Exception as e:
            print(f"Error translating answer to Bengali: {e}")
            self.answer_bn = self.answer

    super().save(*args, **kwargs)

    # After saving, ensure translations are cached for future queries
    if self.question_hi:
        cache.set(f'faq_{self.id}_question_hi', self.question_hi, timeout=86400)
    if self.question_bn:
        cache.set(f'faq_{self.id}_question_bn', self.question_bn, timeout=86400)
    if self.answer_hi:
        cache.set(f'faq_{self.id}_answer_hi', self.answer_hi, timeout=86400)
    if self.answer_bn:
        cache.set(f'faq_{self.id}_answer_bn', self.answer_bn, timeout=86400)
