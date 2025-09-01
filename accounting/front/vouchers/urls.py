from django.urls import path

from . import views

urlpatterns = [
    path("contra/", views.ContraView.as_view(), name="voucher-contra"),
    path("payment/", views.PaymentView.as_view(), name="voucher-payment"),
    path("receipt/", views.ReceiptView.as_view(), name="voucher-receipt"),
    path("journal/", views.JournalView.as_view(), name="voucher-journal"),
    path("purchase/", views.PurchaseView.as_view(), name="voucher-purchase"),
    path("sales/", views.SalesView.as_view(), name="voucher-sales"),
]
