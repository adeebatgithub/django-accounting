from rest_framework.routers import DefaultRouter

from .views import JournalEntryLineViewSet

router = DefaultRouter()

router.register('', JournalEntryLineViewSet)

urlpatterns = router.urls
