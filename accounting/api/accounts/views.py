from rest_framework import viewsets

from accounting.api.accounts.serializers import AccountModelSerializer
from accounting.models import AccountModel


class AccountViewSet(viewsets.ModelViewSet):
    queryset = AccountModel.objects.all()
    serializer_class = AccountModelSerializer
