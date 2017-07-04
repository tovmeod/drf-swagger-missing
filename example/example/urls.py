from django.conf.urls import url, include
from django.contrib import admin

from docs.views import MySwaggerView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/$', MySwaggerView.as_view()),
    url(r'^v1/snippets/', include('snippets.urls'), name='snippets'),
    url(r'^v1/food/', include('food.urls'), name='food'),
]
