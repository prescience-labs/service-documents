import logging

from celery import task
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from common.models import BaseModel
from common.services.text_analysis import TextAnalysis

logger = logging.getLogger(__name__)

class Document(BaseModel, models.Model):
    text = models.TextField()
    sentiment_analysis = JSONField(blank=True, null=True)
    topic_extraction = JSONField(blank=True, null=True)
    categorization = JSONField(blank=True, null=True)
    force_analysis = models.BooleanField(default=False)

@receiver(pre_save, sender=Document)
def get_sentiment_analysis(sender, instance, **kwargs):
    text_analysis = TextAnalysis(instance.text)

    # Prevent sentiment_analysis API call every time the document is saved
    if instance.sentiment_analysis is None or instance.force_analysis:
        instance.sentiment_analysis = text_analysis.get_sentiment_analysis()

    if instance.topic_extraction is None or instance.force_analysis:
        get_topic_extraction.delay(instance.id)

    if instance.categorization is None or instance.force_analysis:
        get_categorization.delay(instance.id)

    instance.force_analysis = False

@task
def get_categorization(document_id):
    logger.debug('get_categorization coming out of the queue')
    document = Document.objects.get(pk=document_id)
    text_analysis = TextAnalysis(document.text)
    document.categorization = text_analysis.get_categorization()
    document.save()

@task
def get_topic_extraction(document_id):
    logger.debug('get_categorization coming out of the queue')
    document = Document.objects.get(pk=document_id)
    text_analysis = TextAnalysis(document.text)
    document.topic_extraction = text_analysis.get_topic_extraction()
    document.save()
