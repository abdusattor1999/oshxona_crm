from rest_framework.routers import DefaultRouter
from .views import OutputViewset

router = DefaultRouter()
# router.register(r'items', OutputItemViewset)
router.register(r'', OutputViewset)