from django.urls import path, include

from .views import UserListCreateAPIView, UserRetrieveUpdateAPIView

auth_urlpatterns = [
    path('', include('dj_rest_auth.urls')),
]

user_urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='list_create'),
    path('<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='retrieve_update'),
]
