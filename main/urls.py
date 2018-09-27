from django.urls import include, path
from rest_framework import routers
from . import views
# from django.contrib.auth import views as auth_views


#AppName 
app_name = 'main'

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'about', views.AboutViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'contact', views.ContactViewSet)
router.register(r'activity', views.ActivityViewSet)
router.register(r'carousel', views.CarouselImageViewSet)
router.register(r'linit', views.LinitViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('users/', views.UserList.as_view(), name='userlist'),
    path('users/<slug:username>/', views.UserDetail.as_view(), name='userdetails'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/createprofile/', views.create_profile, name='createprofile'),
    path('accounts/changeprofile/', views.change_profile, name='changerofile'),
]