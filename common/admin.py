from django.contrib import admin

from common.models import Document

base_readonly_fields = ('id', 'created_at', 'updated_at',)

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = base_readonly_fields + (
        'sentiment_analysis',
        'topic_extraction',
        'categorization',
        'sentiment_analysis_raw',
        'topic_extraction_raw',
        'categorization_raw',
    )
    fieldsets = (
        (None, {
            'fields': ('id', 'created_at', 'updated_at', 'text', 'force_analysis',),
        }),
        ('Analysis', {
            'fields': ('sentiment_analysis', 'topic_extraction', 'categorization',),
        }),
        ('Raw analysis', {
            'fields': ('sentiment_analysis_raw', 'topic_extraction_raw', 'categorization_raw',),
            'classes': ('collapse',),
        }),
    )
admin.site.register(Document, DocumentAdmin)
