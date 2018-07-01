from django.urls import include, path
from rest_framework import routers
from blog import views

app_name = 'blog'

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)


urlpatterns = router.urls