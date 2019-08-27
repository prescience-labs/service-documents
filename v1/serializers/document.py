#pylint: disable=too-few-public-methods,no-self-use
from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models import Document

class DocumentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()

    class Meta:
        model               = Document
        fields              = ['id', 'text', 'sentiment_analysis']
        read_only_fields    = ['sentiment_analysis']
