from rest_framework import serializers

from .models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address']


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'cuisine', 'items', 'price']
