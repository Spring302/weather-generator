from rest_framework.routers import DefaultRouter
from record.views import UserViewSet, DailyRecordViewSet, LoginAccessViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'dailyrecords', DailyRecordViewSet)
router.register(r'loginaccess', LoginAccessViewSet)

urlpatterns = router.urls