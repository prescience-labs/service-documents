#pylint: disable=too-few-public-methods,no-self-use
from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Document
        fields              = '__all__'
        read_only_fields    = ('sentiment_analysis', 'topic_extraction', 'categorization',)
