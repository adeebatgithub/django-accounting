from datetime import datetime

from django import forms

from accounting import models
from .base import VoucherForm
from .utils import get_cash_bank_accounts, get_payment_accounts, get_receipt_accounts, get_purchase_accounts, get_sales_accounts


class ContraForm(VoucherForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account"].queryset = get_cash_bank_accounts()
        self.fields["particulars"].queryset = get_cash_bank_accounts()


class PaymentForm(VoucherForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account"].queryset = get_cash_bank_accounts()
        self.fields["particulars"].queryset = get_payment_accounts()


class ReceiptForm(VoucherForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account"].queryset = get_cash_bank_accounts()
        self.fields["particulars"].queryset = get_receipt_accounts()


class JournalForm(forms.Form):
    reference_number = forms.CharField(max_length=20, required=False)
    date = forms.DateField(initial=datetime.now().date())
    description = forms.CharField(required=False)

    credit_account = forms.ModelChoiceField(queryset=models.AccountModel.objects.all())
    debit_account = forms.ModelChoiceField(queryset=models.AccountModel.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        credit_account = cleaned_data.get("credit_account")
        debit_account = cleaned_data.get("debit_account")

        if date and date > datetime.now().date():
            self.add_error("date", "Date cannot be in the future.")

        if credit_account and debit_account and credit_account == debit_account:
            self.add_error("credit_account", "Both Accounts must be different.")
            self.add_error("debit_account", "Both Accounts must be different.")

        return cleaned_data


class PurchaseForm(VoucherForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account"].queryset = get_cash_bank_accounts()
        self.fields["particulars"].queryset = get_purchase_accounts()


class SalesForm(VoucherForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account"].queryset = get_cash_bank_accounts()
        self.fields["particulars"].queryset = get_sales_accounts()
