from rest_framework import serializers

from accounting.models import AccountModel

class AccountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        exclude = ('slug',)