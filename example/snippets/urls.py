from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from snippets import views

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
]
