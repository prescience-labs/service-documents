from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from common.models import BaseModel
from common.services.text_analysis import TextAnalysis

class Review(BaseModel, models.Model):
    text = models.TextField()
    sentiment_analysis = JSONField(blank=True, null=True)

@receiver(pre_save, sender=Review)
def get_text_analysis(sender, instance, **kwargs):
    text_analysis = TextAnalysis(instance.text)
    instance.sentiment_analysis = text_analysis.sentiment_analysis
