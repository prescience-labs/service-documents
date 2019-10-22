from rest_framework import generics

from common.models import Document
from common.services.auth import user_is_authenticated
from v1.serializers import DocumentSerializer

class DocumentList(generics.ListCreateAPIView):
    queryset            = Document.objects.all()
    serializer_class    = DocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class DocumentDetail(generics.RetrieveAPIView):
    queryset            = Document.objects.all()
    serializer_class    = DocumentSerializer
