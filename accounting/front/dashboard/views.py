from django.db.models import Sum, F
from django.views.generic import TemplateView, ListView

from accounting import models
from accounting.front.utils import get_total_by_type, get_total_by_name
from accounting.front import get_accounts


class DashboardView(TemplateView):
    template_name = "django-accounting/dashboard/dashboard.html"

    @staticmethod
    def get_net_profit():
        return get_total_by_type(models.AccountModel.INCOME) - get_total_by_type(models.AccountModel.EXPENSE)

    def get_closing_capital(self):
        capital_accounts = models.AccountModel.objects.filter(name="Capital Account").get_descendants(include_self=True)
        total_capital = models.JournalEntryLineModel.objects.filter(
            account__in=capital_accounts,
        ).aggregate(
            total=Sum(F('credit') - F('debit'))
        )
        return total_capital['total'] or 0 + self.get_net_profit()

    @staticmethod
    def get_recent_transactions():
        return models.JournalEntryLineModel.objects.select_related('journal_entry'
                                                                   ).order_by('-journal_entry__date')[:10]

    def get_context_data(self, **kwargs):
        return {
            'total_assets': get_total_by_type(models.AccountModel.ASSET),
            'total_liability': get_total_by_type(models.AccountModel.LIABILITY),
            'total_revenue': get_total_by_type(models.AccountModel.INCOME),
            'total_expenses': get_total_by_type(models.AccountModel.EXPENSE),
            'net_profit': self.get_net_profit(),
            'closing_capital': self.get_closing_capital(),

            'recent_transactions': self.get_recent_transactions(),

            'cash_in_hand': get_total_by_name("Cash In Hand"),
            'cash_in_bank': get_total_by_name("Bank Accounts"),
            'current_assets': get_total_by_type(models.AccountModel.ASSET),
            'current_liabilities': get_total_by_type(models.AccountModel.LIABILITY),
            'receivables': get_total_by_name("Accounts Receivable"),
            'payables': get_total_by_name("Accounts Payable"),
        }


class LineListView(ListView):
    template_name = "django-accounting/dashboard/lines.html"
    context_object_name = "transactions"

    def get_queryset(self):
        account_type = self.request.GET.get('type')
        types = {
            "asset": models.AccountModel.ASSET,
            "liability": models.AccountModel.LIABILITY,
            "income": models.AccountModel.INCOME,
            "expenses": models.AccountModel.EXPENSE,
        }
        return models.JournalEntryLineModel.objects.filter(account__account_type=types[account_type])


class SummeryDetailsView(TemplateView):
    template_name = "django-accounting/dashboard/details.html"

    def get_accounts(self):
        kwargs = {
            "cash_in_hand": {"name": "Cash In Hand"},
            "cash_in_bank": {"name": "Bank Accounts"},
            "receivables": {"name": "Accounts Receivable"},
            "payables": {"name": "Accounts Payable"},
            "assets": {"account_type": models.AccountModel.ASSET},
            "liabilities": {"account_type": models.AccountModel.LIABILITY},
        }
        return models.AccountModel.objects.filter(**kwargs.get(self.request.GET.get("particular"))).get_descendants(include_self=True)

    def get_context_data(self, **kwargs):
        return {
            "tabel_heading": self.request.GET.get('particular').replace("_", " ").title(),
            "accounts": self.get_accounts(),
        }
