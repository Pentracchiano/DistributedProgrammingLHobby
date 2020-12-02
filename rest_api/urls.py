from rest_framework import routers
from rest_api.views import *
from rest_framework.authtoken import views
from django.urls import path

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'ongoing_matches', OngoingMatchViewSet)
router.register(r'completed_matches', CompletedMatchViewSet)
urlpatterns = router.urls
urlpatterns += [
    path('token/', views.obtain_auth_token)
]
