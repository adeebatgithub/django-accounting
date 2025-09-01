from tkinter.font import names

from accounting import models


def get_cash_bank_accounts_ids():
    cash_account = models.AccountModel.objects.get(name="Cash In Hand")
    bank_account = models.AccountModel.objects.get(name="Bank Account")

    cash_ids = cash_account.get_descendants(include_self=True).values_list("id", flat=True)
    bank_ids = bank_account.get_descendants(include_self=True).values_list("id", flat=True)
    return list(cash_ids) + list(bank_ids)

def get_cash_bank_accounts():
    pks = get_cash_bank_accounts_ids()
    return models.AccountModel.objects.filter(
        pk__in=get_cash_bank_accounts_ids()
    )

def get_payment_accounts():
    return models.AccountModel.objects.filter(
        account_type__in=[models.AccountModel.LIABILITY, models.AccountModel.EXPENSE]
    )

def get_receipt_accounts():
    return models.AccountModel.objects.filter(
        account_type__in=[models.AccountModel.ASSET, models.AccountModel.INCOME]
    ).exclude(
        pk__in=get_cash_bank_accounts_ids()
    )

def get_purchase_accounts():
    return models.AccountModel.objects.filter(
        name="Purchase Account"
    ).get_descendants(include_self=True)

def get_sales_accounts():
    return models.AccountModel.objects.filter(
        name="Sales Account"
    ).get_descendants(include_self=True)
