#pylint: disable=too-few-public-methods,no-self-use
from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Document
        exclude             = ('sentiment_analysis_raw', 'topic_extraction_raw', 'categorization_raw',)
        read_only_fields    = ('sentiment_analysis', 'topic_extraction', 'categorization',)
