from rest_framework import serializers
from .models import Pizza


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pizza
        fields = ('name', 'paid')
        extra_kwargs = {
            'paid': {'write_only': True}
        }
