from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from rest_framework.reverse import reverse_lazy

from accounting.front.mixins import ApiRequestMixin, FormInvalidMessageMixin
from accounting.front.vouchers.forms import ContraForm, PaymentForm, ReceiptForm, JournalForm, PurchaseForm, SalesForm
from .base import VoucherBaseView
from accounting.front.utils import get_reference_number
from ... import models


class ContraView(VoucherBaseView):
    form_class = ContraForm
    template_name = "django-accounting/vouchers/contra.html"
    success_message = "contra transaction completed"

    def get_entry_description(self, account=None, particulars=None):
        return f"contra transaction from {account} to {particulars}"

    def get_credit_debit(self, account_type=None, amount=None):
        return {
            "account": {
                "credit": float(amount),
            },
            "particulars": {
                "debit": float(amount),
            }
        }


class PaymentView(VoucherBaseView):
    form_class = PaymentForm
    template_name = "django-accounting/vouchers/payment.html"
    success_message = "Payment transaction completed"

    @staticmethod
    def _debit_credit(account_type, amount):
        if account_type in [models.AccountModel.LIABILITY, models.AccountModel.EXPENSE]:
            return {"debit": float(amount)}
        else:
            return {"credit": float(amount)}

    def get_entry_description(self, account=None, particulars=None):
        return f"Payment transaction from {account} to {particulars}"

    def get_credit_debit(self, account_type=None, amount=None):
        return {
            "account": {
                "credit": float(amount),
            },
            "particulars": {
                **self._debit_credit(account_type=account_type, amount=amount),
            }
        }


class ReceiptView(VoucherBaseView):
    form_class = ReceiptForm
    template_name = "django-accounting/vouchers/receipt.html"
    success_message = "Receipt transaction completed"

    def get_entry_description(self, account=None, particulars=None):
        return f"Receipt transaction from {particulars} to {account}"

    def get_credit_debit(self, account_type=None, amount=None):
        return {
            "account": {
                "debit": float(amount),
            },
            "particulars": {
                **self._debit_credit(account_type=account_type, amount=amount),
            }
        }


class JournalView(ApiRequestMixin, FormInvalidMessageMixin, SuccessMessageMixin, generic.FormView):
    form_class = JournalForm
    template_name = "django-accounting/vouchers/journal.html"
    success_message = "Journal transaction completed"
    success_url = reverse_lazy("accounting:daybook")

    def get_success_url(self):
        return reverse_lazy("accounting:daybook")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "reference_number": get_reference_number(),
        })
        return context

    def form_valid(self, form):
        reference_number = form.cleaned_data.get("reference_number")
        date = form.cleaned_data.get("date")
        description = form.cleaned_data.get("description")

        credit_account = form.cleaned_data.get("credit_account")
        debit_account = form.cleaned_data.get("debit_account")
        amount = form.cleaned_data.get("amount")


        entry = self.api_post(url="entry/", data={
            "reference_number": reference_number,
            "date": date.strftime("%Y-%m-%d"),
            "description": description if description else f"journal transaction between {credit_account} and {debit_account}",
        })

        if entry.get("id"):
            self.api_post(url="line/", data={
                "journal_entry": entry["id"],
                "account": credit_account.id,
                "credit": float(amount),
            })
            self.api_post(url="line/", data={
                "journal_entry": entry["id"],
                "account": debit_account.id,
                "debit": float(amount),
            })
        return super().form_valid(form)


class PurchaseView(VoucherBaseView):
    form_class = PurchaseForm
    template_name = "django-accounting/vouchers/purchase.html"
    success_message = "Purchase transaction completed"

    def get_entry_description(self, account=None, particulars=None):
        return f"Purchase transaction from {account} to {particulars}"

    def get_credit_debit(self, account_type=None, amount=None):
        return {
            "account": {
                "credit": float(amount),
            },
            "particulars": {
                "debit": float(amount),
            }
        }


class SalesView(VoucherBaseView):
    form_class = SalesForm
    template_name = "django-accounting/vouchers/purchase.html"
    success_message = "Sales transaction completed"

    def get_entry_description(self, account=None, particulars=None):
        return f"Sales transaction from {account} to {particulars}"

    def get_credit_debit(self, account_type=None, amount=None):
        return {
            "account": {
                "debit": float(amount),
            },
            "particulars": {
                "credit": float(amount),
            }
        }