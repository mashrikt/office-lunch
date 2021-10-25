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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .restaurants.urls import restaurant_urlpatterns, menu_urlpatterns
from .users.urls import auth_urlpatterns, users_urlpatterns
from .votes.urls import vote_urlpatterns, winner_urlpatterns


schema_view = get_schema_view(
   openapi.Info(
      title='Office Lunch API',
      default_version='v1',
      description='Helps Office Decide Their Office Lunch Menu!',
   ),
   public=True,
)

api_patterns = [
    path('auth/', include(arg=(auth_urlpatterns, 'auth'), namespace='auth')),
    path('users/', include(arg=(users_urlpatterns, 'users'), namespace='users')),
    path('restaurants/', include(arg=(restaurant_urlpatterns, 'restaurants'), namespace='restaurants')),
    path('menus/', include(arg=(menu_urlpatterns, 'menus'), namespace='menus')),
    path('votes/', include(arg=(vote_urlpatterns, 'votes'), namespace='votes')),
    path('winners/', include(arg=(winner_urlpatterns, 'winners'), namespace='winners')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include(arg=(api_patterns, 'api_patterns'), namespace='api')),
]
