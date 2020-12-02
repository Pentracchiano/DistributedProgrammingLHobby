from rest_framework import routers
from rest_api.views import *

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'ongoing_matches', OngoingMatchViewSet)
router.register(r'completed_matches', CompletedMatchViewSet)
urlpatterns = router.urls
