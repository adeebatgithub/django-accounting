from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView, ListView

from accounting import models
from accounting.front.utils import get_total


class ProfitLossListView(TemplateView):
    template_name = "django-accounting/reports/profit_loss.html"

    def get_context_data(self, **kwargs):
        return {
            "income_accounts": models.AccountModel.objects.filter(account_type=models.AccountModel.INCOME).annotate(
                total_credit=Coalesce(Sum("journalentrylinemodel__credit"), Value(0), output_field=DecimalField()),
                total_debit=Coalesce(Sum("journalentrylinemodel__debit"), Value(0), output_field=DecimalField()),
            ),
            "net_income": get_total(models.AccountModel.INCOME),
            "expense_accounts": models.AccountModel.objects.filter(account_type=models.AccountModel.EXPENSE).annotate(
                total_credit=Coalesce(Sum("journalentrylinemodel__credit"), Value(0), output_field=DecimalField()),
                total_debit=Coalesce(Sum("journalentrylinemodel__debit"), Value(0), output_field=DecimalField()),
            ),
            "net_expense": get_total(models.AccountModel.EXPENSE),
            "net_profit": get_total(models.AccountModel.INCOME) - get_total(models.AccountModel.EXPENSE),
        }


class BalanceSheet(TemplateView):
    template_name = "django-accounting/reports/balancesheet.html"

    def get_context_data(self, **kwargs):
        return {
            "asset_accounts": models.AccountModel.objects.filter(account_type=models.AccountModel.ASSET),
            "liability_accounts": models.AccountModel.objects.filter(account_type=models.AccountModel.LIABILITY),
            "total_asset": get_total(models.AccountModel.ASSET),
            "total_liability": get_total(models.AccountModel.LIABILITY),
        }


class TrialBalance(ListView):
    model = models.JournalEntryLineModel
    template_name = "django-accounting/reports/trialbalance.html"
    context_object_name = "transactions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "total_debit": models.JournalEntryLineModel.objects.all().aggregate(
                sum=Sum("debit"),
            )["sum"],
            "total_credit": models.JournalEntryLineModel.objects.all().aggregate(
                sum=Sum("credit"),
            )["sum"],
        })
        return context
