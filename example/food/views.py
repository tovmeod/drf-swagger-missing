import coreapi

from drf_swagger_missing import coreschema
# make sure to import coreschema from drf_swagger_missing to be sure it is already patched
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework import renderers
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from food.models import Pizza
from .permissions import IsOwnerOrReadOnly
from .serializers import PizzaSerializer


class PizzaViewSet(viewsets.ModelViewSet):
    """
    retrieve: My own text
    I can write the description here
    """
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    class Meta:
        # defines responses for each action
        responses = {
            'review': [
                coreschema.Response(status=status.HTTP_202_ACCEPTED, description='Review accepted',
                                    schema=coreschema.Object(
                                        properties=[
                                            coreschema.String(title='job',
                                                              description='The job url/id, '
                                                                          'query this to see the job status.')])),
                coreschema.Response(status=status.HTTP_404_NOT_FOUND, description='pizza doesn\'t exist ',
                                    schema=coreschema.String()),
                coreschema.Response(status=status.HTTP_400_BAD_REQUEST,
                                    description='Your review is not valid',
                                    schema=coreschema.String()),
                coreschema.Response(status='default',
                                    description='Swagger may have default response',
                                    schema=coreschema.Object()),
            ],
            'retrieve': [coreschema.Response(status=status.HTTP_404_NOT_FOUND, description='pizza doesn\'t exist ',
                                    schema=coreschema.String())]
        }
        fields = {'review': [
            coreapi.Field(name='stars', required=False, location='query', schema=coreschema.Number()),
            coreapi.Field(name='picture', required=False, location='query', schema=coreschema.File()),
        ]}
        produces = {'review': ["image/png", 'application/json']}

    def get_serializer_class(self):
        if self.action == 'review':
            return serializers.Serializer
        return super().get_serializer_class()

    @detail_route(methods=['post'])
    def review(self):
        """Users can upload a review"""
        return Response({'status': 'password set'})
