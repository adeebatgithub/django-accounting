from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('transactions/', views.LineListView.as_view(), name='dashboard-transactions'),
]
