from django.urls import path

from .views import (
    RestaurantListCreateAPIView,
    RestaurantRetrieveUpdateAPIView,
    MenuListCreateAPIView,
    MenuRetrieveUpdateDestroyAPIView
)


restaurant_urlpatterns = [
    path('', RestaurantListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', RestaurantRetrieveUpdateAPIView.as_view(), name='retrieve_update'),
]

menu_urlpatterns = [
    path('', MenuListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', MenuRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update'),
]
