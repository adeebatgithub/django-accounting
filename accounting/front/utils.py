from django.db.models import Sum, Case, F, When, DecimalField

from accounting.models import JournalEntryModel, AccountModel, JournalEntryLineModel


def get_reference_number():
    last_entry = JournalEntryModel.objects.all().last()
    if last_entry and last_entry.reference_number.isdigit():
        return str(int(last_entry.reference_number) + 1).zfill(6)
    return "000001"


def get_total_by_type(account_type):
    accounts = AccountModel.objects.filter(account_type=account_type)
    return JournalEntryLineModel.objects.filter(account__in=accounts).aggregate(
        total=Sum(
            Case(
                When(account__account_type__in=[AccountModel.ASSET, AccountModel.EXPENSE],
                     then=F('debit') - F('credit')),
                When(account__account_type__in=[AccountModel.LIABILITY, AccountModel.INCOME],
                     then=F('credit') - F('debit')),
                default=0,
                output_field=DecimalField()
            )
        )
    )['total'] or 0


def get_total_by_name(name):
    accounts = AccountModel.objects.get(name=name).get_descendants(include_self=True)
    return JournalEntryLineModel.objects.filter(account__in=accounts).aggregate(
        total=Sum(
            Case(
                When(account__account_type__in=[AccountModel.ASSET, AccountModel.EXPENSE],
                     then=F('debit') - F('credit')),
                When(account__account_type__in=[AccountModel.LIABILITY, AccountModel.INCOME],
                     then=F('credit') - F('debit')),
                default=0,
                output_field=DecimalField()
            )
        )
    )['total'] or 0
