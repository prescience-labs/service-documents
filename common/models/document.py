import logging
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from common.services.text_analysis import TextAnalysis

logger = logging.getLogger(__name__)

class Document(BaseModel):
    text                    = models.TextField()
    sentiment_analysis      = JSONField(blank=True, null=True, help_text=_("SERIALIZED: From MeaningCloud's Sentiment Analysis"))
    sentiment_analysis_raw  = JSONField(blank=True, null=True, help_text=_("From MeaningCloud's Sentiment Analysis"))
    topic_extraction        = JSONField(blank=True, null=True, help_text=_("SERIALIZED: From MeaningCloud's Topic Extraction"))
    topic_extraction_raw    = JSONField(blank=True, null=True, help_text=_("From MeaningCloud's Topic Extraction"))
    categorization          = JSONField(blank=True, null=True, help_text=_("SERIALIZED: From MeaningCloud's Deep Categorization"))
    categorization_raw      = JSONField(blank=True, null=True, help_text=_("From Meaningcloud's Deep Categorization"))
    force_analysis          = models.BooleanField(default=False, help_text=_('Run all analyses during the next analysis job.'))

    def get_sentiment_analysis(self):
        text_analysis = TextAnalysis(self.text)
        text_analysis.get_sentiment_analysis()

        self.sentiment_analysis     = text_analysis.sentiment_analysis
        self.sentiment_analysis_raw = text_analysis.sentiment_analysis_raw

    def get_topic_extraction(self):
        text_analysis = TextAnalysis(self.text)
        text_analysis.get_topic_extraction()

        self.topic_extraction       = text_analysis.topic_extraction
        self.topic_extraction_raw   = text_analysis.topic_extraction_raw

    def get_categorization(self):
        text_analysis = TextAnalysis(self.text)
        text_analysis.get_categorization()

        self.categorization     = text_analysis.categorization
        self.categorization_raw = text_analysis.categorization_raw


@receiver(pre_save, sender=Document)
def get_sentiment_analysis(sender, instance, **kwargs):
    """Get sentiment analysis immediately on document save"""
    text_analysis = TextAnalysis(instance.text)

    # Prevent sentiment_analysis API call every time the document is saved
    if instance.sentiment_analysis is None:
        instance.get_sentiment_analysis()
