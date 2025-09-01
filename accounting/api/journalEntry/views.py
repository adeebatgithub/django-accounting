from rest_framework import viewsets

from accounting.api.journalEntry.serializers import JournalEntryModelSerializer
from accounting.models import JournalEntryModel


class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntryModel.objects.all()
    serializer_class = JournalEntryModelSerializer
