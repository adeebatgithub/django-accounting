from rest_framework import serializers

from accounting.models import JournalEntryModel

class JournalEntryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntryModel
        fields = "__all__"