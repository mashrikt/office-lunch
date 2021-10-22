from django.urls import path, include

from .views import UserListCreateAPIView, UserRetrieveUpdateAPIView

auth_urlpatterns = [
    path('', include('dj_rest_auth.urls')),
]

users_urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='list_create_users'),
    path('<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='retrieve_update_user'),
]
