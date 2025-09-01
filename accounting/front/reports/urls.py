from django.urls import path

from . import views

urlpatterns = [
    path("profit-loss/", views.ProfitLossListView.as_view(), name="report-profit-loss"),
    path("balance-sheet/", views.BalanceSheet.as_view(), name="report-balance-sheet"),
    path("trial-balance/", views.TrialBalance.as_view(), name="report-trial-balance"),
]
