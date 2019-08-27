from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from common.models import Document

class Command(BaseCommand):
    help = 'Runs available analyses on all documents without analyses'

    def handle(self, *args, **options):
        documents = Document.objects.filter(
            Q(sentiment_analysis__isnull=True)
            | Q(topic_extraction__isnull=True)
            | Q(categorization__isnull=True)
            | Q(force_analysis=True)
        )

        for document in documents:
            try:
                if document.sentiment_analysis is None or document.force_analysis:
                    self.stdout.write(self.style.NOTICE(f'Getting sentiment analysis for {document.id}'))
                    document.get_sentiment_analysis()
                if document.topic_extraction is None or document.force_analysis:
                    self.stdout.write(self.style.NOTICE(f'Getting topic extraction for {document.id}'))
                    document.get_topic_extraction()
                if document.categorization is None or document.force_analysis:
                    self.stdout.write(self.style.NOTICE(f'Getting categorization for {document.id}'))
                    document.get_categorization()
                document.force_analysis = False
                document.save()
            except:
                raise RuntimeError('Error getting text analysis for documents.')
        self.stdout.write(self.style.SUCCESS('Successfully analyzed documents.'))
