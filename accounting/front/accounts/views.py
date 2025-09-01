from datetime import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Case, When, F, IntegerField
from django.shortcuts import redirect
from django.views import generic
from rest_framework.reverse import reverse_lazy
from django.utils.text import slugify

from accounting import models
from accounting.front.accounts import forms
from accounting.front.mixins import ApiRequestMixin, FormInvalidMessageMixin
from accounting.front.utils import get_reference_number


class AccountsView(generic.TemplateView):
    template_name = 'django-accounting/accounts/chart.html'

    @staticmethod
    def get_queryset(account_type):
        return models.AccountModel.objects.filter(account_type=account_type).order_by('tree_id', 'lft')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "asset_accounts": self.get_queryset(models.AccountModel.ASSET),
            "liability_accounts": self.get_queryset(models.AccountModel.LIABILITY),
            "income_accounts": self.get_queryset(models.AccountModel.INCOME),
            "expense_accounts": self.get_queryset(models.AccountModel.EXPENSE),
        })
        return context


class AccountDetailView(generic.DetailView):
    model = models.AccountModel
    template_name = "django-accounting/accounts/details.html"
    context_object_name = "account"

    def get_account_balance(self):
        totals = self.object.journalentrylinemodel_set.aggregate(
            total_debit=Sum('debit'),
            total_credit=Sum('credit'),
        )
        debit = totals['total_debit'] or 0
        credit = totals['total_credit'] or 0

        if self.object.account_type in [models.AccountModel.ASSET, models.AccountModel.EXPENSE]:
            balance = debit - credit
        else:  # Liability, Income
            balance = credit - debit

        return balance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "transactions": models.JournalEntryLineModel.objects.filter(account=self.object),
            "balance": self.get_account_balance(),
        })
        return context


class AccountCreateView(ApiRequestMixin, FormInvalidMessageMixin, SuccessMessageMixin, generic.CreateView):
    model = models.AccountModel
    form_class = forms.AccountUpsertForm
    template_name = "django-accounting/accounts/create.html"
    success_message = "Account created Successfully"

    def get_success_url(self):
        return reverse_lazy("accounting:account-details", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "accounts": models.AccountModel.objects.only("id", "name"),
        })
        return context

    @staticmethod
    def _debit_credit(account_type, amount):
        if account_type in [models.AccountModel.LIABILITY, models.AccountModel.INCOME]:
            return {"credit": float(amount)}
        else:
            return {"debit": float(amount)}

    def form_valid(self, form):
        name = form.cleaned_data['name']
        parent = form.cleaned_data['parent']
        account_type = form.cleaned_data['account_type']
        opening_balance = form.cleaned_data['opening_balance']

        account = self.api_post(url="accounts/", data={
            "name": name,
            "parent": parent.id if parent else None,
            "account_type": account_type,
        })

        if opening_balance != 0:
            entry = self.api_post(url="entry/", data={
                "date": datetime.now().strftime("%Y-%m-%d"),
                "reference_number": get_reference_number(),
                "description": f"opening balance of {name}",
            })

            self.api_post(url="line/", data={
                "journal_entry": entry.get("id"),
                "account": account.get("id"),
                **self._debit_credit(account_type, opening_balance),
            })

        self.object = models.AccountModel.objects.get(id=account.get("id"))
        return redirect(self.get_success_url())


class AccountUpdateView(ApiRequestMixin, FormInvalidMessageMixin, SuccessMessageMixin, generic.UpdateView):
    model = models.AccountModel
    form_class = forms.AccountUpsertForm
    template_name = "django-accounting/accounts/update.html"
    context_object_name = "account"
    success_message = "Account updated successfully"

    def get_success_url(self):
        return reverse_lazy("accounting:account-details", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "accounts": models.AccountModel.objects.only("id", "name"),
            "opening_balance": models.JournalEntryLineModel.objects.filter(
                account=self.object,
                journal_entry__description__contains=f"opening balance of {self.object.name}"
            ).aggregate(
                balance=Sum(
                    Case(
                        When(debit=0, then=F("credit")),
                        When(credit=0, then=F("debit")),
                        default=0,
                        output_field=IntegerField(),
                    )
                )
            )["balance"]
        })
        print(context['form'])
        return context

    @staticmethod
    def _debit_credit(account_type, amount):
        if account_type in [models.AccountModel.LIABILITY, models.AccountModel.INCOME]:
            return {"credit": str(amount), "debit": 0}
        else:
            return {"debit": str(amount), "credit": 0}

    def get_entry_id(self):
        line = models.JournalEntryLineModel.objects.filter(
            account=self.object, journal_entry__description__icontains=f"opening balance"
        )
        if line.exists():
            return {"entry_id": line.first().journal_entry.id, "line_id": line.first().id}
        return None

    def form_valid(self, form):
        name = form.cleaned_data['name']
        parent = form.cleaned_data['parent']
        account_type = form.cleaned_data['account_type']
        opening_balance = form.cleaned_data['opening_balance']

        account = self.api_put(url=f"accounts/{self.object.id}/", data={
            "name": name,
            "parent": parent.id if parent else None,
            "account_type": account_type,
        })

        if opening_balance:
            entry = self.get_entry_id()
            if not entry:
                entry = self.api_post(url=f"entry/", data={
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "reference_number": get_reference_number(),
                    "description": f"opening balance of {name}",
                })

                self.api_post(url="line/", data={
                    "journal_entry": entry.get("id"),
                    "account": account.get("id"),
                    **self._debit_credit(account_type, opening_balance),
                })
            else:
                self.api_patch(url=f"entry/{entry.get('entry_id')}/", data={
                    "description": f"opening balance of {name}",
                })
                self.api_patch(url=f"line/{entry.get('line_id')}/", data={
                    **self._debit_credit(account_type, opening_balance),
                })

        self.object = form.save(commit=False)
        return redirect(self.get_success_url())


class AccountDeleteView(ApiRequestMixin, SuccessMessageMixin, generic.DeleteView):
    model = models.AccountModel
    success_url = reverse_lazy("accounting:account-chart")
    success_message = "Account Deleted Successfully"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.api_delete(url=f"accounts/{self.object.id}/")
        return redirect(self.get_success_url())
