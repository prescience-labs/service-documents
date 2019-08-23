from django.contrib import admin

from common.models import Document

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('sentiment_analysis', 'topic_extraction', 'categorization')
admin.site.register(Document, DocumentAdmin)
