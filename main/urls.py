from django.urls import include, path
from rest_framework import routers
from . import views
from main.views import EventViewSet, ProfileViewSet, UserViewSet, AboutViewSet


#AppName 
app_name = 'main'

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'about', AboutViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('users/', views.UserList.as_view(), name='userlist'),
    path('users/<slug:username>/', views.UserDetail.as_view(), name='userdetails'),
]