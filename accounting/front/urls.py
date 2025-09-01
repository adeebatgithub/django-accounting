from django.urls import path, include
from django.views.generic import RedirectView

from .views import DayBookListView
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="accounting:dashboard")),

    path('daybook/', DayBookListView.as_view(), name='daybook'),
    path('dashboard/', include('accounting.front.dashboard.urls')),
    path('accounts/', include('accounting.front.accounts.urls')),
    path('vouchers/', include('accounting.front.vouchers.urls')),
    path('reports/', include('accounting.front.reports.urls')),
]