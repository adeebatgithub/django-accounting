from tkinter.font import names

from django.views.generic import ListView

from accounting import models
from accounting.front.get_accounts import get_cash_bank_accounts

class DayBookListView(ListView):
    queryset = models.JournalEntryLineModel.objects.all()
    template_name = "django-accounting/daybook.html"
    context_object_name = "transactions"

    def get_queryset(self):
        book_type = self.request.GET.get('book_type')
        if book_type == "all":
            return self.queryset

        elif book_type in ("sales", "purchases"):
            account_names = {
                "sales": "Sales Account",
                "purchases": "Purchase Account",
            }
            accounts = models.AccountModel.objects.filter(name=account_names.get(book_type)).get_descendants(include_self=True)
            return models.JournalEntryLineModel.objects.filter(account__in=accounts)

        elif book_type == "cash":
            return models.JournalEntryLineModel.objects.filter(account__in=get_cash_bank_accounts())

        elif book_type == "general":
            sales_accounts = models.AccountModel.objects.filter(name="Sales Account").get_descendants(include_self=True)
            purchases_accounts = models.AccountModel.objects.filter(name="Purchase Account").get_descendants(include_self=True)
            cash_bank_accounts = get_cash_bank_accounts()
            accounts = list(sales_accounts) + list(purchases_accounts) + list(cash_bank_accounts)
            return models.JournalEntryLineModel.objects.exclude(account__in=accounts)
