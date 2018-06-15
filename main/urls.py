from django.urls import include, path
from rest_framework import routers

from main.views import EventViewSet, ProfileViewSet, UserViewSet


#AppName 
app_name = 'main'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = router.urls