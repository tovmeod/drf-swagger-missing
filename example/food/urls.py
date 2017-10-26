from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from food import views

router = DefaultRouter()
router.register(r'pizzas', views.PizzaViewSet)
router.register(r'toppings', views.ToppingViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^(?P<bucket_id>\w+)[.](?P<file_format>\w+)$', views.BucketView.as_view({'get': 'retrieve'}), name='tile'),
    # url(r'^(?P<bucket_id>\w+)[.](?P<file_format>\w+)/metadata$',
    #     views.BucketMetadataView.as_view({'get': 'retrieve'}), name='tile_meta'),
    # url(r'^(?P<bucket_id>\w+)[.](?P<file_format>\w+)/pixeldata$',
    #     views.BucketPixelView.as_view({'get': 'retrieve'}), name='pixel_data'),
    # url(r'^(?P<bucket_id>\w+)[.](?P<file_format>\w+)/pixelhistory$',
    #     views.BucketPixelHistoryView.as_view({'get': 'retrieve'}),
    #     name='pixel_history'),
    # url(r'^(?P<bucket_id>\w+)/ingest/(?P<plan_name>\w+)$', views.BucketPlanView.as_view(),
    #     name="plan_view"),
]
