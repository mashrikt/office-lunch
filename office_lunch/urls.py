"""office_lunch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .restaurants.urls import restaurant_urlpatterns, menu_urlpatterns
from .users.urls import auth_urlpatterns, users_urlpatterns

api_patterns = [
    path('auth/', include(arg=(auth_urlpatterns, 'auth'), namespace='auth')),
    path('users/', include(arg=(users_urlpatterns, 'users'), namespace='users')),
    path('restaurants/', include(arg=(restaurant_urlpatterns, 'restaurants'), namespace='restaurants')),
    path('menus/', include(arg=(menu_urlpatterns, 'menus'), namespace='menus')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(arg=(api_patterns, 'api_patterns'), namespace='api')),
]
