from django.urls import path

from . import views

urlpatterns = [
    path('chart/', views.AccountsView.as_view(), name='account-chart'),
    path('chart/<slug>/', views.AccountDetailView.as_view(), name='account-details'),
    path('create/', views.AccountCreateView.as_view(), name='account-create'),
    path('update/<slug>/', views.AccountUpdateView.as_view(), name='account-update'),
    path('delete/<slug>/', views.AccountDeleteView.as_view(), name='account-delete'),
]
