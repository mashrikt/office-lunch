from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from .models import Restaurant, Menu
from .permissions import IsAdminUserOrReadOnly
from .serializers import RestaurantSerializer, MenuSerializer


class RestaurantListCreateAPIView(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_fields = ('date', 'restaurant')


class MenuRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
