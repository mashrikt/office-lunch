from rest_framework import serializers

from .models import Restaurant, Menu
from .relations import PresentablePrimaryKeyRelatedField


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address']


class MenuSerializer(serializers.ModelSerializer):

    restaurant = PresentablePrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        presentation_serializer=RestaurantSerializer
    )

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'cuisine', 'items', 'price']
