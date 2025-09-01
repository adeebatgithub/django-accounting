from django.urls import path, include

urlpatterns = [
    path('', include('accounting.front.urls')),
    path('api/', include('accounting.api.urls'))
]