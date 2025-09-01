from django.db.models import Sum, F
from django.views.generic import TemplateView, ListView

from accounting import models
from accounting.front.utils import get_total


class DashboardView(TemplateView):
    template_name = "django-accounting/dashboard/dashboard.html"

    @staticmethod
    def get_net_profit():
        return get_total(models.AccountModel.INCOME) - get_total(models.AccountModel.EXPENSE)

    def get_closing_capital(self):
        capital_accounts = models.AccountModel.objects.filter(name="Capital Account").get_descendants(include_self=True)
        total_capital = models.JournalEntryLineModel.objects.filter(
            account__in=capital_accounts,
        ).aggregate(
            total=Sum(F('credit') - F('debit'))
        )
        return total_capital['total'] + self.get_net_profit()

    @staticmethod
    def get_recent_transactions():
        return models.JournalEntryLineModel.objects.select_related('journal_entry'
                                                                   ).order_by('-journal_entry__date')[:10]

    def get_context_data(self, **kwargs):
        return {
            'total_assets': get_total(models.AccountModel.ASSET),
            'total_liability': get_total(models.AccountModel.LIABILITY),
            'total_revenue': get_total(models.AccountModel.INCOME),
            'total_expenses': get_total(models.AccountModel.EXPENSE),
            'net_profit': self.get_net_profit(),
            'closing_capital': self.get_closing_capital(),
            'recent_transactions': self.get_recent_transactions(),
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
