from rest_framework import serializers

from accounting.models import JournalEntryLineModel

class JournalEntryLineModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntryLineModel
        fields = "__all__"