from django.core.management import BaseCommand

from accounting.models import AccountModel
from accounting.etc.accounts import LIST_OF_ACCOUNTS

class Command(BaseCommand):
    def _account_exists(self, account_name):
        return AccountModel.objects.filter(name=account_name).exists()

    def create_account(self, **kwargs):
        if self._account_exists(kwargs['name']):
            self.stdout.write(f'Account Exists: {kwargs['name']}')
            return

        obj = AccountModel.objects.create(**kwargs)
        self.stdout.write(f'Account created: {obj.name} under > {obj.parent}')

    def handle(self, *args, **options):
        for account in LIST_OF_ACCOUNTS:
            self.create_account(**account)

        self.stdout.write(f"Total accounts Created: {AccountModel.objects.count()}")