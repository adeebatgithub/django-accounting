from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('summery/details/', views.SummeryDetailsView.as_view(), name='dashboard-summery-details'),
    path('transactions/', views.LineListView.as_view(), name='dashboard-transactions'),
]
