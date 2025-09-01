from rest_framework import viewsets

from accounting.api.journalEntryLine.serializers import JournalEntryLineModelSerializer
from accounting.models import JournalEntryLineModel


class JournalEntryLineViewSet(viewsets.ModelViewSet):
    queryset = JournalEntryLineModel.objects.all()
    serializer_class = JournalEntryLineModelSerializer
