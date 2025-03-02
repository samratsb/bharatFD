# Generated by Django 5.1.5 on 2025-02-02 17:10

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='answer'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question_bn',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='faq',
            name='question_hi',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
