from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounting.api.accounts.urls')),
    path('entry/', include('accounting.api.journalEntry.urls')),
    path('line/', include('accounting.api.journalEntryLine.urls'))
]