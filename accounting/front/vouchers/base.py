from datetime import datetime
from decimal import Decimal

from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounting import models
from accounting.front.mixins import ApiRequestMixin, FormInvalidMessageMixin
from accounting.front.utils import get_reference_number
from accounting.models import AccountModel


class VoucherBaseView(ApiRequestMixin, FormInvalidMessageMixin, SuccessMessageMixin, FormView):
    entry_description = None
    credit_debit = {}

    def get_credit_debit(self, account_type=None, amount=None):
        if self.credit_debit:
            if not self.credit_debit.get("account") or not self.credit_debit.get("particulars"):
                return ImproperlyConfigured(
                    f"{self.__class__.__name__}: cannot find account, particulars in credit_debit")
            return self.credit_debit
        return ImproperlyConfigured(f"{self.__class__.__name__}: implement credit_debit")

    def get_entry_description(self, account=None, particulars=None):
        if self.entry_description:
            return self.entry_description
        return ImproperlyConfigured(f"{self.__class__.__name__}: implement entry_description")

    def get_success_url(self):
        return f"{reverse_lazy("accounting:daybook")}?book_type=all"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "reference_number": get_reference_number(),
        })
        return context

    @staticmethod
    def _debit_credit(account_type, amount):
        if account_type in [models.AccountModel.LIABILITY, models.AccountModel.INCOME]:
            return {"credit": float(amount)}
        else:
            return {"debit": float(amount)}

    def form_valid(self, form):
        reference_number = form.cleaned_data['reference_number']
        date = form.cleaned_data['date']
        account = form.cleaned_data['account']
        particulars = form.cleaned_data['particulars']
        amount = form.cleaned_data['amount']
        description = form.cleaned_data['description']

        entry = self.api_post(url="entry/", data={
            "reference_number": reference_number,
            "date": date.strftime("%Y-%m-%d"),
            "description": description if description else f"{self.get_entry_description(account=account.name, particulars=particulars.name)}",
        })

        self.api_post(url="line/", data={
            "journal_entry": entry.get("id"),
            "account": account.id,
            **self.get_credit_debit(account_type=account.account_type, amount=amount).get("account"),
        })
        self.api_post(url="line/", data={
            "journal_entry": entry.get("id"),
            "account": particulars.id,
            **self.get_credit_debit(account_type=particulars.account_type, amount=amount).get("particulars"),
        })

        return super().form_valid(form)


class VoucherForm(forms.Form):
    reference_number = forms.CharField(max_length=20, required=False)
    date = forms.DateField(initial=datetime.now().date())
    account = forms.ModelChoiceField(queryset=None)
    particulars = forms.ModelChoiceField(queryset=None)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        account = cleaned_data.get("account")
        particulars = cleaned_data.get("particulars")
        amount = cleaned_data.get("amount")
        trx_date = cleaned_data.get("date")

        if account and particulars and account == particulars:
            self.add_error("particulars", "Account and Particulars must be different.")

        if amount is not None and amount <= Decimal("0.00"):
            self.add_error("amount", "Amount must be greater than zero.")

        if trx_date and trx_date > datetime.now().date():
            self.add_error("date", "Date cannot be in the future.")

        if amount and amount > account.get_balance():
            self.add_error("account", "Account balance is low")

        return cleaned_data


class BaseJournalFormset(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_debit = 0
        total_credit = 0

        form_number = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False) and form.cleaned_data.get("id", False):
                print(form.cleaned_data)
                debit = form.cleaned_data.get("debit") or 0
                credit = form.cleaned_data.get("credit") or 0
                account = form.cleaned_data.get("account")
                if account.account_type in [AccountModel.LIABILITY, AccountModel.INCOME] and debit > account.get_balance():
                    raise forms.ValidationError("Account balance is low")

                if account.account_type in [AccountModel.ASSET, AccountModel.EXPENSE] and credit > account.get_balance():
                    raise forms.ValidationError("Account balance is low")

                total_debit += debit
                total_credit += credit
            form_number += 1

        if total_debit != total_credit:
            raise forms.ValidationError("Total debit must equal total credit.")
