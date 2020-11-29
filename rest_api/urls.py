from rest_framework import routers
from rest_api.views import *

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls
