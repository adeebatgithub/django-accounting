from django.core.management import BaseCommand

from accounting.models import AccountModel
from accounting.etc.accounts import LIST_OF_ACCOUNTS

class Command(BaseCommand):
    def create_account(self, **kwargs):
        obj = AccountModel.objects.create(**kwargs)
        self.stdout.write(f'Account created: {obj.name} under > {obj.parent}')

    def handle(self, *args, **options):
        for account in LIST_OF_ACCOUNTS:
            self.create_account(**account)

        self.stdout.write(f"Total accounts Created: {AccountModel.objects.count()}")